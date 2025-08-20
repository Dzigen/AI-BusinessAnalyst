from dataclasses import dataclass, field
from typing import Tuple
from copy import deepcopy
import gc

from ....utils import Logger, AgentTaskSolverConfig, AgentTaskSolver, ReturnStatus
from ....db_drivers.kv_driver import KeyValueDriverConfig
from ....agents import AgentDriver, AgentDriverConfig
from ....specification_model import ReqSpecificationModel
from ....specification_model.utils import Scenario
from ..utils import AbstractNaiveModule, NaiveReasonerStatus, NaiveGlobalSignal, NaiveStateSignal
from ...utils import BAResponse, UserResponse, DialogueHistory, Response
from .config import BA_SCENARIOS_CLARIFYING_NOTICE, BA_FIXING_USERSTORY_NOTICE, \
    BA_SCENARIOS_LIMIT_NOTICE, BA_ALLSTORIES_CLARIFIED_NOTICE, DEFAULT_CSG_TASK_CONFIG, SC_STATE_SIGNALSINFO
from .utils import ScenariosClarifierState
from ..config import NBAR_GLOBAL_SIGNALSINFO


SEXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/naive/s_extractor/main'

@dataclass
class ScenariosClarifierConfig:
    scenarios_per_user_story_limit: int = 5

    lang: str = "ru"
    adriver_config: AgentDriverConfig = field(default_factory=lambda: AgentDriverConfig())
    condsgen_task_config: AgentTaskSolverConfig = field(default_factory=lambda: DEFAULT_CSG_TASK_CONFIG)

    log: Logger = field(default_factory=lambda: Logger(SEXTRACTOR_MAIN_LOG_PATH))
    verbose: bool = False

class ScenariosClarifier(AbstractNaiveModule):
    def __init__(self, reqspec_model: ReqSpecificationModel, 
                 config: ScenariosClarifierConfig = ScenariosClarifierConfig(), 
                 mode: str = 'prod', cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config
        self.reqspec_model = reqspec_model
        self.mode = mode
        self.us_dialogue_history = dict()

        self.init_module_state()

        self.agent = AgentDriver.connect(config.adriver_config)
        self.condsgen_solver = AgentTaskSolver(
            self.agent, self.config.condsgen_task_config, cache_kvdriver_config)
        
        self.log = self.config.log
        self.verbose = self.config.verbose

    def init_module_state(self):
        self.state = ScenariosClarifierState.greetings
        self.continue_operation = False
        self.next_stage = False
        self.user_stories_ids = None
        self.current_us_idx = -1
        self.curmax_scenario_id = 0
        self.cur_us_id = None
        self.cur_us_text = None
        self.current_scenarios_count = 0
        del self.us_dialogue_history 
        self.us_dialogue_history = dict()
        gc.collect()

    def prepare_response(self) -> Tuple[BAResponse, NaiveReasonerStatus]:
        self.user_stories_ids = list(self.reqspec_model.specification_struct.user_stories.keys())
        ba_response, new_status = None, None
        if self.state == ScenariosClarifierState.greetings:
            ba_response = BAResponse(ba_text=BA_SCENARIOS_CLARIFYING_NOTICE, 
                                     available_global_signals=[NBAR_GLOBAL_SIGNALSINFO['next_stage']])
            self.state = ScenariosClarifierState.fixing_userstory
            new_status = NaiveReasonerStatus.waiting_interaction
        
        elif self.state == ScenariosClarifierState.fixing_userstory:
            self.current_us_idx += 1
            if self.current_us_idx >= len(self.user_stories_ids):
                self.state = ScenariosClarifierState.done
                ba_response = BAResponse(ba_text=BA_ALLSTORIES_CLARIFIED_NOTICE, 
                                         available_global_signals=[NBAR_GLOBAL_SIGNALSINFO['next_stage']])
                new_status = NaiveReasonerStatus.done
            else:
                self.cur_us_id = self.user_stories_ids[self.current_us_idx]
                self.cur_us_text = self.reqspec_model.specification_struct.user_stories[self.cur_us_id].statement
                self.us_dialogue_history[self.cur_us_id] = DialogueHistory()
                self.current_scenarios_count = 0
                self.curmax_scenario_id = 0

                self.state = ScenariosClarifierState.clarifying_scenario
                ba_response = BAResponse(ba_text=BA_FIXING_USERSTORY_NOTICE.format(us_id=self.cur_us_id, us_text=self.cur_us_text))
                new_status = NaiveReasonerStatus.waiting_interaction

        elif self.state == ScenariosClarifierState.clarifying_scenario:
            if self.current_scenarios_count > self.config.scenarios_per_user_story_limit:
                self.state = ScenariosClarifierState.fixing_userstory
                ba_response = BAResponse(ba_text=BA_SCENARIOS_LIMIT_NOTICE)
                new_status = NaiveReasonerStatus.waiting_interaction
            else:
                if self.mode == 'prod':
                    scenario, status = self.condsgen_solver.solve(
                        lang=self.config.lang, user_story=self.cur_us_text, 
                        dialogue_history=self.us_dialogue_history[self.cur_us_id])
                    if status != ReturnStatus.success:
                        # TODO: Предложить обработчик ошибки парсинга ответа LLM
                        raise ValueError
                elif self.mode == 'stub':
                    scenario = "Пример сценария"
                else:
                    raise ValueError

                ba_response = BAResponse(ba_text=scenario,
                                         available_global_signals=[NBAR_GLOBAL_SIGNALSINFO['next_stage']],
                                         available_state_signals=[SC_STATE_SIGNALSINFO['next_scenario']])
                self.us_dialogue_history[self.cur_us_id].sequence.append(Response(role='ba', text=ba_response.ba_text))
                new_status = NaiveReasonerStatus.waiting_response
                self.current_scenarios_count += 1

        else:
            raise AttributeError

        return ba_response, new_status

    def process_response(self, user_response: UserResponse) -> NaiveReasonerStatus:
        new_status = None
        if self.state == ScenariosClarifierState.clarifying_scenario:
            if user_response.signal is not None:
                self.continue_operation = user_response.signal == NaiveStateSignal.continue_operation
                self.next_stage = user_response.signal == NaiveGlobalSignal.next_stage
                new_status = NaiveReasonerStatus.waiting_interaction

                if self.continue_operation:
                    self.state = ScenariosClarifierState.fixing_userstory
                elif self.next_stage:
                    self.state = ScenariosClarifierState.done
                    new_status = NaiveReasonerStatus.done
                else:
                    raise ValueError

            elif user_response.user_text is not None:
                self.us_dialogue_history[self.cur_us_id].sequence.append(Response(role='user',text=user_response.user_text))
                if user_response.user_text.lower() == 'да':
                    self.curmax_scenario_id += 1
                    scenario_id = f"{self.current_us_idx+1}.{self.curmax_scenario_id}"
                    self.reqspec_model.specification_struct.scenarios[scenario_id] = \
                        Scenario(id=scenario_id, statement=self.us_dialogue_history[self.cur_us_id].sequence[-2].text)
                elif user_response.user_text.lower() == 'нет':
                    pass
                else:
                    # TODO
                    raise NotImplementedError
                new_status = NaiveReasonerStatus.waiting_interaction

            else:
                raise ValueError
        else:
            raise AttributeError

        return new_status

    def reset(self):
        self.init_module_state()
    