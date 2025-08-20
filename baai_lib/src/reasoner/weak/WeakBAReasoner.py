from dataclasses import dataclass, field
from typing import Union, Dict
from .config import WEAKBAREASONER_MAIN_LOG_PATH
from .utils import WeakReasonerState, WeakReasonerStatus
from ..utils import AbstractBAReasoner, BAResponse, UserResponse
from ...utils import Logger
from ...db_drivers.kv_driver import KeyValueDriverConfig
from ...specification_model import ReqSpecificationModel

from .states_handlers import InitCommunicator, InitCommunicatorConfig, \
    TaskGeneralCommunicator, TaskGeneralCommunicatorConfig, BusinessProcessesCommunicator, BusinessProcessesCommunicatorConfig, \
        UserStoriesCommunicator, UserStoriesCommunicatorConfig, RolesCommunicator, RolesCommunicatorConfig, \
            ScenariosCommunicator, ScenariosCommunicatorConfig, FuncRequirementsCommunicator, FuncRequirementsCommunicatorConfig, \
                FuncRestrictionsCommunicator, FuncRestrictionsCommunicatorConfig, SysRequirementsCommunicator, SysRequirementsCommunicatorConfig, \
                    SysRestrictionsCommunicator, SysRestrictionsCommunicatorConfig, DoneCommunicator, DoneCommunicatorConfig

@dataclass
class WeakBAReasonerConfig:
    init_communicator_config: InitCommunicatorConfig = field(default_factory=lambda: InitCommunicatorConfig())

    task_clarifier_config: TaskGeneralCommunicatorConfig = field(default_factory=lambda: TaskGeneralCommunicatorConfig())
    bp_clarifier_config: BusinessProcessesCommunicatorConfig = field(default_factory=lambda: BusinessProcessesCommunicatorConfig())
    
    us_clarifier_config: UserStoriesCommunicatorConfig = field(default_factory=lambda: UserStoriesCommunicatorConfig())
    r_extractor_config: RolesCommunicatorConfig = field(default_factory=lambda: RolesCommunicatorConfig())
    s_clarifier_config: ScenariosCommunicatorConfig = field(default_factory=lambda: ScenariosCommunicatorConfig())
    
    funcreqs_extractor_config: FuncRequirementsCommunicatorConfig = field(default_factory=lambda: FuncRequirementsCommunicatorConfig())
    funcrestr_clarifier_config: FuncRestrictionsCommunicatorConfig = field(default_factory=lambda: FuncRestrictionsCommunicatorConfig())
    
    sysreqs_clarifier_config: SysRequirementsCommunicatorConfig = field(default_factory=lambda: SysRequirementsCommunicatorConfig())
    sysrestr_clarifier_config: SysRestrictionsCommunicatorConfig = field(default_factory=lambda: SysRestrictionsCommunicatorConfig())
    
    done_config: DoneCommunicatorConfig = field(default_factory=lambda: DoneCommunicatorConfig())
    done_config: DoneCommunicatorConfig = field(default_factory=lambda: DoneCommunicatorConfig())
    
    mode: str = 'stub' # 'stub' | 'dev'
    log: Logger = field(default_factory=lambda: Logger(WEAKBAREASONER_MAIN_LOG_PATH))
    verbose: bool = False

class WeakBAReasoner(AbstractBAReasoner):

    def __init__(self, reqspec_model: ReqSpecificationModel, config: WeakBAReasonerConfig = WeakBAReasonerConfig(), 
                 cache_kvdriver_config: KeyValueDriverConfig = None):
        self.config = config

        self.init_interaction_states(reqspec_model, cache_kvdriver_config)

    def init_interaction_states(self, reqspec_model: ReqSpecificationModel, cache_kvdriver_config: KeyValueDriverConfig = None):
        self.REASONER_STATUS = WeakReasonerStatus.waiting_interaction 
        self.REASONER_STATE = WeakReasonerState.init
        self.__REASONER_STATE_INDEX__ = 0
        self.reqspec_model = reqspec_model

        if cache_kvdriver_config is not None:
            self.cache_kvdriver_config = cache_kvdriver_config

        self.MODULES_MAP = {
            WeakReasonerState.init: InitCommunicator(self.config.init_communicator_config),
            WeakReasonerState.task_clarifying: TaskGeneralCommunicator(reqspec_model, self.config.task_clarifier_config, self.config.mode),
            WeakReasonerState.bp_clarifying: BusinessProcessesCommunicator(reqspec_model, self.config.bp_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.userstories_crud: UserStoriesCommunicator(reqspec_model, self.config.us_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.roles_extracting: RolesCommunicator(reqspec_model, self.config.r_extractor_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.scenarios_ccrud: ScenariosCommunicator(reqspec_model, self.config.s_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.funcreq_extracting: FuncRequirementsCommunicator(reqspec_model, self.config.funcreqs_extractor_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.funcrestr_ccrud: FuncRestrictionsCommunicator(reqspec_model, self.config.funcrestr_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.sysreq_crud: SysRequirementsCommunicator(reqspec_model, self.config.sysreqs_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.sysrestr_ccrud: SysRestrictionsCommunicator(reqspec_model, self.config.sysrestr_clarifier_config, self.config.mode, self.cache_kvdriver_config),
            WeakReasonerState.done: DoneCommunicator(reqspec_model, self.config.done_config, self.config.mode)
        }

        self.MODULES_MAP[WeakReasonerState.done_unsupported_task] = self.MODULES_MAP[WeakReasonerState.done]

        self.MODULES_EXECUTION_SEQUENCE = [
            WeakReasonerState.init, WeakReasonerState.task_clarifying, WeakReasonerState.bp_clarifying, 
            WeakReasonerState.userstories_crud, WeakReasonerState.roles_extracting, WeakReasonerState.scenarios_ccrud, 
            WeakReasonerState.funcreq_extracting, WeakReasonerState.funcrestr_ccrud, WeakReasonerState.sysreq_crud, WeakReasonerState.sysrestr_ccrud, 
            WeakReasonerState.done]

        for module_name in self.MODULES_MAP.keys():
            self.MODULES_MAP[module_name].init_state()

    def change_mode_to(self, new_mode: str = 'stub') -> None:
        self.config.mode = new_mode
        for module_name in self.MODULES_EXECUTION_SEQUENCE[:-1]:
            self.MODULES_MAP[module_name].mode = self.config.mode

    def change_state(self, direction: str = 'forward') -> None:
        if direction == 'forward':
            self.__REASONER_STATE_INDEX__ += 1
        else:
            raise ValueError
        
        self.REASONER_STATE = self.MODULES_EXECUTION_SEQUENCE[self.__REASONER_STATE_INDEX__]

    def prepare_response(self) -> BAResponse:
        if self.REASONER_STATUS != WeakReasonerStatus.waiting_interaction:
            raise ValueError

        self.REASONER_STATUS = WeakReasonerStatus.processing
        ba_response, new_rstatus, done_state = self.MODULES_MAP[self.REASONER_STATE].prepare_response()
        
        if done_state is not None:
            self.REASONER_STATUS = new_rstatus
            self.REASONER_STATE = done_state 

        elif new_rstatus == WeakReasonerStatus.done:
            self.change_state(direction='forward')
            self.REASONER_STATUS = WeakReasonerStatus.waiting_interaction

        else:
            self.REASONER_STATUS = new_rstatus

        return ba_response

    def process_response(self, user_response: UserResponse) -> None:
        if self.REASONER_STATUS != WeakReasonerStatus.waiting_response:
            raise ValueError
        
        self.REASONER_STATUS = WeakReasonerStatus.processing
        self.MODULES_MAP[self.REASONER_STATE].process_response(user_response)
        self.REASONER_STATUS = WeakReasonerStatus.waiting_interaction

    def get_task_description(self, format: str = 'markdown') -> Union[Dict[str,Union[Dict[str,str], str]],str]:
        formated_description = None

        if format == 'markdown':
            #
            taskgoal_subsection = "\n## Назначение проект\n\n{taskgoal}"
            merged_taskgoal = taskgoal_subsection.format(taskgoal=self.reqspec_model.specification_struct.general.goal)
            
            subtasks_subsection = "\n## Основные задачи\n\n{subtasks}"
            merged_subtasks = subtasks_subsection.format(subtasks=self.reqspec_model.specification_struct.general.sub_tasks)

            integration_subsection = "\n## Интеграция со сторонними системами\n\n{integr}"
            merged_integration = integration_subsection.format(integr=self.reqspec_model.specification_struct.general.integration)

            #
            funcreq_subsection = "\n## Функциональные требования\n\n{funcreq}"
            str_freq_groups = []
            for fgroup in self.reqspec_model.specification_struct.reqs_info.fgroups.values():
                cur_str_freqs = []
                for freq_id in fgroup.grouped_funcreq_ids:
                    cur_freq = self.reqspec_model.specification_struct.reqs_info.functional[freq_id]
                    cur_str_freq = f"{cur_freq.statement} (ФТ# {cur_freq.id})"
                    cur_str_freqs.append(cur_str_freq)
                
                numerated_freqs = "\n".join([f"{i+1}. {str_freq}" for i, str_freq in enumerate(cur_str_freqs)])
                cur_str_freq_group = f"**{fgroup.title}**\n{numerated_freqs}"
                str_freq_groups.append(cur_str_freq_group)
            formated_freq_groups = "\n\n".join(str_freq_groups)
            merged_funcreq = funcreq_subsection.format(funcreq=formated_freq_groups)

            nonfuncreq_subsection = "\n## Функциональные ограничения\n\n{nonfuncreq}"
            str_nonfuncreq = list(map(lambda item: f"{item.statement} (НФТ# {item.id})", self.reqspec_model.specification_struct.reqs_info.functional_restrictions.values()))
            formated_nonfuncreq = '\n'.join([f"{i+1}. {nonfuncreq}" for i, nonfuncreq in enumerate(str_nonfuncreq)])
            merged_nonfuncreq = nonfuncreq_subsection.format(nonfuncreq=formated_nonfuncreq)

            #
            userstories_subsection = "\n## Модель предметной области\n\n{userstories}"
            str_userstories = list(map(lambda item: f"{item.statement} (ПИ# {item.id})", self.reqspec_model.specification_struct.user_stories.values()))
            formated_userstories = '\n'.join([f"{i+1}. {userstory}" for i, userstory in enumerate(str_userstories)])
            merged_userstories = userstories_subsection.format(userstories=formated_userstories)

            roles_subsection = "\n## Модели пользователей системы\n\n### Виды пользователей:\n\n{roles}"
            str_roles = list(map(lambda item: f"{item.name}", self.reqspec_model.specification_struct.roles.values()))
            formated_roles = "\n".join([f"* {role}" for role in str_roles])
            merged_roles = roles_subsection.format(roles=formated_roles)

            scenarios_subsection = "\n## Функциональная модель\n\n{scenarios}"
            str_scenarios = []
            for scenario in self.reqspec_model.specification_struct.scenarios.values():
                str_title = f"**Сценарий: {scenario.title}** (СИ# {scenario.id})"
                str_steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(scenario.steps)])
                str_scenario = f"{str_title}\n{str_steps}"
                str_scenarios.append(str_scenario)
            formated_scenarios = '\n\n'.join(str_scenarios)
            merged_scenarios = scenarios_subsection.format(scenarios=formated_scenarios)

            #
            sysreq_subsection = "\n## Системные требования\n\n{sysreq}"
            formated_sysreq = '\n'.join(list(map(lambda item: f"{item[0]+1}. {item[1].statement} (CТ# {item[1].id})", enumerate(self.reqspec_model.specification_struct.system_info.requirements.values()))))
            merged_sysreq = sysreq_subsection.format(sysreq=formated_sysreq)

            nonsysreq_subsection = "\n## Системные ограничения\n\n{nonsysreq}"
            formated_nonsysreq = '\n'.join(list(map(lambda item: f"{item[0]+1}. {item[1].statement} (НCТ# {item[1].id})", enumerate(self.reqspec_model.specification_struct.system_info.restrictions.values()))))
            merged_nonsysreq = nonsysreq_subsection.format(nonsysreq=formated_nonsysreq)

            sep_line = "------------------------------"
            general_part = f"# План проекта\n{merged_taskgoal}\n{merged_subtasks}\n{merged_integration}"
            reqs_part = f"# Первичный список требований\n{merged_funcreq}\n{merged_nonfuncreq}"
            models_part = f"# Модели требований\n{merged_userstories}\n{merged_roles}\n{merged_scenarios}"
            arch_part = f"# Высокоуровневая архитектура системы\n{merged_sysreq}\n{merged_nonsysreq}"

            formated_description = f"{general_part}\n\n{sep_line}\n\n{reqs_part}\n\n{sep_line}\n\n{models_part}\n\n{sep_line}\n\n{arch_part}"

        elif format == 'dict':
            # TODO
            raise NotImplementedError
        
        else:
            raise ValueError
        
        return formated_description

    def reset(self, reqspec_model: ReqSpecificationModel):
        self.init_interaction_states(reqspec_model)
