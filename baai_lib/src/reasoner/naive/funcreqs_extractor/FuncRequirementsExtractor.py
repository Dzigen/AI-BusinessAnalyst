from dataclasses import dataclass, field
from typing import Tuple

from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ....specification_model import ReqSpecificationModel
from ....agents import AgentDriver, AgentDriverConfig
from ....specification_model.utils import FunctionalRequirement
from ..utils import AbstractNaiveModule, NaiveReasonerStatus
from .config import BA_FUNCREQ_EXTRACT_NOTICE, DEFAULT_CFG_TASK_CONFIG, BA_EXTRACTED_FREQ_NOTICE
from ...utils import BAResponse, UserResponse, DialogueHistory
from .utils import FuncRequirementsExtractorState

FREQEXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/naive/freq_extractor/main'

@dataclass
class FuncRequirementsExtractorConfig:
    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condfgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CFG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(FREQEXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class FuncRequirementsExtractor(AbstractNaiveModule):
    def __init__(self, dialogue_history: DialogueHistory, reqspec_model: ReqSpecificationModel,
                  config: FuncRequirementsExtractorConfig = FuncRequirementsExtractorConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.dialogue_history = dialogue_history
        self.mode = mode

        self.init_module_state()

        self.agent = AgentDriver.connect(self.config.adriver_config)
        self.condfgen_solver = AgentTaskSolver(
            self.agent, self.config.condfgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = FuncRequirementsExtractorState.greetings

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        ba_response, new_status = None, None
        if self.state == FuncRequirementsExtractorState.greetings:
            ba_response = BAResponse(ba_text=BA_FUNCREQ_EXTRACT_NOTICE)
            new_status = NaiveReasonerStatus.waiting_interaction
            self.state = FuncRequirementsExtractorState.extracting

        elif self.state == FuncRequirementsExtractorState.extracting:
            self.reqspec_model.specification_struct.edit_count += 1
            gen_freq_count = 0
            for scenario in self.reqspec_model.specification_struct.scenarios.values():
                if self.mode == 'prod':
                    func_reqs, status = self.condfgen_solver.solve(
                        lang=self.config.lang, scenario=scenario.statement, dialogue_history=self.dialogue_history)
                    if status != ReturnStatus.success:
                        # TODO: Предложить обработчик ошибки парсинга ответа LLM
                        raise ValueError
                elif self.mode == 'stub':
                    func_reqs = ["Функциональное требование №1", "Функциональное требование №2"]
                else:
                    # TODO
                    pass
                
                gen_freq_count += len(func_reqs)
                for i, nonfreq in enumerate(func_reqs):
                    nonfreq_id = f"{scenario.id}.{i+1}"
                    self.reqspec_model.specification_struct.reqs_info.functional[nonfreq_id] = \
                        FunctionalRequirement(id=nonfreq_id, statement=nonfreq)

            ba_response = BAResponse(ba_text=BA_EXTRACTED_FREQ_NOTICE.format(freq_amount=gen_freq_count))
            new_status = NaiveReasonerStatus.done
            self.state = FuncRequirementsExtractorState.done
        else:
            raise ValueError
        
        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> None:
        # TODO
        raise NotImplementedError
    
    def reset(self):
        self.init_module_state()