from .utils import USExtractingState, USAddState, USEditState, USDeleteState, USClarifierState, USClarifierCurrentState
from ....utils import SignalInfo
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...utils import WeakStateSignal
from ...config import WBAR_GLOBAL_SIGNALSINFO

USCOMMUNICATOR_MAIN_LOG_PATH = 'log/reasoner/weak/us_communicator/main'

BAUSC_MESSAGE_TAMPLATES = {
    'start_us_clarify': "Приступаю к уточнению пользовательских историй.",
    'start_us_extraction': "Начинаю извлечение пользовательских историй на основе предоставленной информации.", 
    'us_extraction_results': "Извлечено пользовательских историй: {us_amount}.", 
    'select_us_edit_notice': "Вы можете, при необходимости, редактировать, добавлять или удалять пользовательские истории.", 
    'add': {
        'start_add': "Запускаю операцию добавления новой пользовательской истории.", 
        'request_input': "Пожалуйста, введите новую пользовательскую историю.",
        'bad_input_notice': "Не удалось добавить пользовательскую историю.",
        'add_notice': "Пользовательская история успешно добавлена.",
        'stop_add': "Операция по добавлению новой пользовательской истории завершена.",
    },
    'delete': {
        "start_delete": "Запускаю операцию удаления пользовательской истории.",
        "select_us_notice": "Пожалуйста, введите идентификатор пользовательской истории, которую необходимо удалить.",
        "bad_select_notice": "Не удалось выбрать пользовательскую историю.",
        "delete_notice": "История успешно удалена.",
        "stop_delete": "Операция по удалению пользовательской истории завершена.",
    },
    'edit': {
        "start_edit": "Запускаю операцию редактирования пользовательской истории.",
        "select_us_notice": "Пожалуйста, введите идентификатор пользовательской истории, которую необходимо отредактировать.",
        "bad_select_notice": "Не удалось выбрать пользовательскую историю.",
        "request_input": "Введите новую формулировку пользовательской истории.",
        "bad_editing_notice": "Не удалось сохранить изменения.",
        "editing_notice": "Изменения успешно сохранены.", 
        "stop_edit": "Операция по редактированию пользовательской истории завершена.",
    },
    'stop_us_clarify': "Уточнение пользовательских историй завершено." 
}

WUSC_SELECT_STATE_SIGNALSINFO = {
    'create': SignalInfo(
        signal=WeakStateSignal.add,
        shortcut="Добавить user-историю"
    ),
    'delete': SignalInfo(
        signal=WeakStateSignal.delete,
        shortcut="Удалить user-историю"
    ),
    'update': SignalInfo(
        signal=WeakStateSignal.edit,
        shortcut="Изменить user-историю"
    )
}

WUSC_CUD_STATE_SIGNALSINFO = {
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

BAUSC_RESPONSE_CONFIG = {
    USClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BAUSC_MESSAGE_TAMPLATES['start_us_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=USClarifierCurrentState(
            base_state=USClarifierState.us_extracting,
            usextr_state=USExtractingState.init
        )
    ),
    
    USClarifierState.us_extracting: {
        USExtractingState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['start_us_extraction'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.us_extracting,
                usextr_state=USExtractingState.done
            )
        ),
        USExtractingState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['us_extraction_results'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.select_act
            )
        )
    },

    USClarifierState.select_act: StateAction(
        ba_response=BAResponse(
            ba_text=BAUSC_MESSAGE_TAMPLATES['select_us_edit_notice'],
            available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values()),
            available_state_signals=list(WUSC_SELECT_STATE_SIGNALSINFO.values()),
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_response,
        stage_newstate=USClarifierCurrentState(
            base_state=USClarifierState.select_act
        )
    ),

    USClarifierState.add: {
        USAddState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['add']['start_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.add,
                usadd_state=USAddState.adding_us
            )
        ),
        
        USAddState.adding_us: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['add']['request_input'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.add,
                usadd_state=USAddState.adding_us
            )
        ),
        
        USAddState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['add']['bad_input_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.add,
                    usadd_state=USAddState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['add']['add_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.add,
                    usadd_state=USAddState.done
                )
            )
        },

        USAddState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['add']['stop_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.select_act,
            )
        )
    },

    USClarifierState.delete: {
        USDeleteState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['delete']['start_delete'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.delete,
                usdelete_state=USDeleteState.us_selecting
            )
        ),
        
        USDeleteState.us_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['delete']["select_us_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.delete,
                usdelete_state=USDeleteState.us_selecting
            )
        ),
        
        USDeleteState.usid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['delete']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.delete,
                    usdelete_state=USDeleteState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['delete']["delete_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.delete,
                    usdelete_state=USDeleteState.done
                )
            ),
        },
        
        USDeleteState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['delete']["stop_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.select_act,
            )
        )
    },

    USClarifierState.edit: {
        USEditState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["start_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.edit,
                usedit_state=USEditState.us_selecting
            )
        ),

        USEditState.us_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["select_us_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.edit,
                usedit_state=USEditState.us_selecting
            )
        ),

        USEditState.usid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.edit,
                    usedit_state=USEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.edit,
                    usedit_state=USEditState.editing_us
                )
            ),
        },

        USEditState.editing_us: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["request_input"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False, 
                user_base_answer=..., # FILLED DYNAMICALLY
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.edit,
                usedit_state=USEditState.editing_us
            )
        ),

        USEditState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["bad_editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.edit,
                    usedit_state=USEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=USClarifierCurrentState(
                    base_state=USClarifierState.edit,
                    usedit_state=USEditState.done
                )
            ),
        },

        USEditState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAUSC_MESSAGE_TAMPLATES['edit']["stop_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=USClarifierCurrentState(
                base_state=USClarifierState.select_act
            )
        ),
    },

    USClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BAUSC_MESSAGE_TAMPLATES['stop_us_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=USClarifierCurrentState(
            base_state=USClarifierState.done
        )
    ),
}