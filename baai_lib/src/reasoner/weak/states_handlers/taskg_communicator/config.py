from .utils import TaskGeneralCommunicatorState, TGCTaskClassifyingState, \
    TGClarifierCurrentState, TGCInfoExtractingState, TGCAskingState
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...config import WBAR_GLOBAL_SIGNALSINFO

TCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/weak/taskg_communicator/main'

BATC_MESSAGE_TAMPLATES = {
    'general_clarification_notice': "Сейчас я задам вам несколько общих вопросов, чтобы лучше понять задачу.",
    'stop_general_clarification_notice': "Отлично, на этом общие вопросы закончены.",
    'tcls_state': {
        'start_cls_notice': "Анализирую описание задачи.",
        'cls_result': "По результатам анализа, генерация технического задания по вашему описанию {t_cls}.",
        'stop_cls_notice': "Процесс анализа завершён."
    },
    'info_extr_state': {
        'start_extr_notice': "Начинаю формирование секции технического задания с общей информацией по проекту.",
        'goal_extraction_notice': "Формирую раздел ТЗ с описанием назначение проекта.",
        'goal_extraction_result': "Раздел сформирован.",
        'subt_extraction_notice': "Формирую раздел ТЗ с описанием основных задач в рамках проекта.",
        'subt_extraction_result': "Раздел сформирован.",
        'integr_extraction_notice': "Формирую раздел ТЗ с описанием интеграционных моментов.",
        'integr_extraction_result': "Раздел сформирован.",
        'stop_extr_notice': "Cекция с общей информацией по проекту сформирована."
    },
    'continue_tclr': "Перейдём к уточнению деталей."
}


BATC_RESPONSE_CONFIG = {
    TaskGeneralCommunicatorState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BATC_MESSAGE_TAMPLATES['general_clarification_notice'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=TGClarifierCurrentState(
            base_state=TaskGeneralCommunicatorState.clarifying
        )
    ),

    TaskGeneralCommunicatorState.clarifying: {
        TGCAskingState.question_preparing: StateAction(
            ba_response=BAResponse(
                    ba_text=..., # FILLED DYNAMICALLY
                    available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values())
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.clarifying,
                askq_state=TGCAskingState.question_preparing
            )
        ),
        TGCAskingState.limit_exceeded: StateAction(
            ba_response=BAResponse(
                    ba_text=BATC_MESSAGE_TAMPLATES['stop_general_clarification_notice'],
                    is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.task_classifying,
                askq_state=TGCAskingState.limit_exceeded
            )
        )
    },

    TaskGeneralCommunicatorState.task_classifying: {
        TGCTaskClassifyingState.init: StateAction(
            ba_response=BAResponse(
                    ba_text=BATC_MESSAGE_TAMPLATES['tcls_state']['start_cls_notice'],
                    is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.task_classifying,
                tcls_state=TGCTaskClassifyingState.classifying
            )
        ),
        TGCTaskClassifyingState.classifying: StateAction(
            ba_response=BAResponse(
                    ba_text=BATC_MESSAGE_TAMPLATES['tcls_state']['cls_result'],
                    is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.task_classifying,
                tcls_state=TGCTaskClassifyingState.done
            )
        ),
        TGCTaskClassifyingState.done: StateAction(
            ba_response=BAResponse(
                    ba_text=BATC_MESSAGE_TAMPLATES['tcls_state']['stop_cls_notice'],
                    is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=... # FILLED DYNAMICALLY
            )
        ),
    },

    TaskGeneralCommunicatorState.info_extracting: {
        TGCInfoExtractingState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['start_extr_notice'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.goal_extr_notice
            )
        ),
        TGCInfoExtractingState.goal_extr_notice: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['goal_extraction_notice'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.goal_extr_process
            )
        ),
        TGCInfoExtractingState.goal_extr_process: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['goal_extraction_result'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.subt_extr_notice
            )
        ),
        TGCInfoExtractingState.subt_extr_notice: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['subt_extraction_notice'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.subt_extr_process
            )
        ),
        TGCInfoExtractingState.subt_extr_process: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['subt_extraction_result'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.integr_extr_notice
            )
        ),
        TGCInfoExtractingState.integr_extr_notice: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['integr_extraction_notice'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.integr_extr_process
            )
        ),
        TGCInfoExtractingState.integr_extr_process: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['integr_extraction_result'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.info_extracting,
                iextr_state=TGCInfoExtractingState.done
            )
        ),
        TGCInfoExtractingState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BATC_MESSAGE_TAMPLATES['info_extr_state']['stop_extr_notice'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=TGClarifierCurrentState(
                base_state=TaskGeneralCommunicatorState.done
            )
        ),
    },

    TaskGeneralCommunicatorState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BATC_MESSAGE_TAMPLATES['continue_tclr'],
            is_userinput_locked=True),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=TGClarifierCurrentState(
            base_state=TaskGeneralCommunicatorState.done)),

}

TASK_GENERAL_QUESTIONS = [
    "Опишите вашу задачу простыми словами.",
    "Какую проблему вы хотите решить с помощью продукта?",
    "Какой результат вы ожидаете? (Что должно быть на выходе?)",
    "Кто будет пользоваться продуктом? (Целевая аудитория)",
    "Есть ли предпочтения по технологиям или ограничения?",
    "Какие данные уже есть, и какие данные нужно собирать?",
    "Есть ли интеграции с другими системами?",
    "Какие есть дополнительные пожелания или требования?"
]