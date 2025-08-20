from dataclasses import dataclass, field
from typing import Tuple

from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ....specification_model import ReqSpecificationModel
from ....agents import AgentDriver, AgentDriverConfig
from ....specification_model.utils import NonFunctionalReuqirement
from ..utils import AbstractNaiveModule, NaiveReasonerStatus
from ...utils import BAResponse, UserResponse, DialogueHistory
from .config import BA_NONFUNCREQ_EXTRACT_NOTICE, DEFAULT_CNONFG_TASK_CONFIG, BA_EXTRACTED_NONFREQ_NOTICE
from .utils import NonFuncRequirementsExtractorState

NFREQEXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/naive/nfreq_extractor/main'

@dataclass
class NonFuncRequirementsExtractorConfig:
    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condnfgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CNONFG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(NFREQEXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class NonFuncRequirementsExtractor(AbstractNaiveModule):
    def __init__(self, dialogue_history: DialogueHistory, reqspec_model: ReqSpecificationModel, 
                  config: NonFuncRequirementsExtractorConfig = NonFuncRequirementsExtractorConfig(), 
                  mode:str = "prod", cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.dialogue_history = dialogue_history
        self.mode = mode

        self.init_module_state()

        self.agent = AgentDriver.connect(config.adriver_config)
        self.condnfgen_solver = AgentTaskSolver(
            self.agent, self.config.condnfgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = NonFuncRequirementsExtractorState.greetings

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_status = None, None
        if self.state == NonFuncRequirementsExtractorState.greetings:
            ba_response = BAResponse(ba_text=BA_NONFUNCREQ_EXTRACT_NOTICE)
            new_status = NaiveReasonerStatus.waiting_interaction
            self.state = NonFuncRequirementsExtractorState.extracting

        elif self.state == NonFuncRequirementsExtractorState.extracting:
            self.reqspec_model.specification_struct.edit_count += 1
            gen_nonfreq_count = 0
            for scenario in self.reqspec_model.specification_struct.scenarios.values():
                if self.mode == 'prod':
                    nonfunc_reqs, status = self.condnfgen_solver.solve(
                        lang=self.config.lang, scenario=scenario.statement, dialogue_history=self.dialogue_history)
                    if status != ReturnStatus.success:
                        # TODO: Предложить обработчик ошибки парсинга ответа LLM
                        raise ValueError
                elif self.mode == 'stub':
                    nonfunc_reqs = ["Нефункциональное требование №1", "Нефункциональное требование №2"]
                else:
                    raise ValueError
                
                gen_nonfreq_count += len(nonfunc_reqs)
                for i, nonfreq in enumerate(nonfunc_reqs):
                    nonfreq_id = f"{scenario.id}.{i+1}"
                    self.reqspec_model.specification_struct.reqs_info.non_functional[nonfreq_id] = \
                        NonFunctionalReuqirement(id=nonfreq_id, statement=nonfreq)
             
            ba_response = BAResponse(ba_text=BA_EXTRACTED_NONFREQ_NOTICE.format(nonfreq_amount=gen_nonfreq_count))
            new_status = NaiveReasonerStatus.done
            self.state = NonFuncRequirementsExtractorState.done
        else:
            raise AttributeError
        
        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> None:
        # TODO
        raise NotImplementedError
    
    def reset(self):
        self.init_module_state