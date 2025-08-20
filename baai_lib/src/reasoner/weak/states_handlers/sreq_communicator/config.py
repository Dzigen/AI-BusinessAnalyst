from ....utils import SignalInfo
from ...utils import WeakStateSignal
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from .utils import SReqAddState, SReqClarifierCurrentState, SReqClarifierState, \
    SReqDeleteState, SReqEditState, SReqExtractingState
from ...config import WBAR_GLOBAL_SIGNALSINFO

SREQEXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/weak/sreq_communicator/main'

BASREQ_MESSAGE_TAMPLATES = {
    'start_sr_clarify': "Приступаю к формированию системных требований.", 
    'start_sr_extraction': "Начинаю извлечение системных требований.", 
    'sr_extraction_results': "Извлечено системных требований: {sr_amount}.", 
    'select_sr_edit_notice': "Вы можете, при необходимости, редактировать, добавлять или удалять системные требования.", 
    'add': {
        'start_add': "Запускаю операцию добавления нового системного требования.", 
        'request_input': "Пожалуйста, введите новое системное требование.", 
        'bad_input_notice': "Не удалось добавить системное требование.", 
        'add_notice': "Системное требование успешно добавлено.", 
        'stop_add': "Операция по добавлению нового системного требования завершена.", 
    },
    'delete': {
        "start_delete": "Запускаю операцию удаления системного требования.", 
        "select_sr_notice": "Пожалуйста, введите идентификатор системного требования, которое необходимо удалить.", 
        "bad_select_notice": "Не удалось выбрать системное требование.", 
        "delete_notice": "Требование успешно удалено.", 
        "stop_delete": "Операция по удалению системного требования завершена.", 
    },
    'edit': {
        "start_edit": "Запускаю операцию редактирования системного требования.", 
        "select_sr_notice": "Пожалуйста, введите идентификатор системного требования, которого необходимо отредактировать.", 
        "bad_select_notice": "Не удалось выбрать системное требование.", 
        "request_input": "Введите новую формулировку системного требования.", 
        "bad_editing_notice": "Не удалось сохранить изменения.", 
        "editing_notice": "Изменения успешно сохранены.", 
        "stop_edit": "Операция по редактированию системного требования завершена.", 
    },
    'stop_sr_clarify': "Формирование системных требований завершено."  
}

WUSC_SELECT_STATE_SIGNALSINFO = {
    'create': SignalInfo(
        signal=WeakStateSignal.add,
        shortcut="Добавить требование"
    ),
    'delete': SignalInfo(
        signal=WeakStateSignal.delete,
        shortcut="Удалить требование"
    ),
    'update': SignalInfo(
        signal=WeakStateSignal.edit,
        shortcut="Изменить требование"
    )
}

WUSC_CUD_STATE_SIGNALSINFO = {
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

BASREQC_MESSAGE_TAMPLATES = {
    SReqClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BASREQ_MESSAGE_TAMPLATES['start_sr_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=SReqClarifierCurrentState(
            base_state=SReqClarifierState.sreq_extracting,
            srextr_state=SReqExtractingState.init
        )
    ),
    
    SReqClarifierState.sreq_extracting: {
        SReqExtractingState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['start_sr_extraction'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.sreq_extracting,
                srextr_state=SReqExtractingState.done
            )
        ),
        SReqExtractingState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['sr_extraction_results'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.select_act
            )
        )
    },

    SReqClarifierState.select_act: StateAction(
        ba_response=BAResponse(
            ba_text=BASREQ_MESSAGE_TAMPLATES['select_sr_edit_notice'],
            available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values()),
            available_state_signals=list(WUSC_SELECT_STATE_SIGNALSINFO.values()),
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_response,
        stage_newstate=SReqClarifierCurrentState(
            base_state=SReqClarifierState.select_act
        )
    ),

    SReqClarifierState.add: {
        SReqAddState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['add']['start_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.add,
                sradd_state=SReqAddState.adding_sreq
            )
        ),
        
        SReqAddState.adding_sreq: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['add']['request_input'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.add,
                sradd_state=SReqAddState.adding_sreq
            )
        ),

        SReqAddState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['add']['bad_input_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.add,
                    sradd_state=SReqAddState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['add']['add_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.add,
                    sradd_state=SReqAddState.done
                )
            )
        },

        SReqAddState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['add']['stop_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.select_act,
            )
        )
    },

    SReqClarifierState.delete: {
        SReqDeleteState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['delete']['start_delete'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.delete,
                srdelete_state=SReqDeleteState.sreq_selecting
            )
        ),
        
        SReqDeleteState.sreq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['delete']["select_sr_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.delete,
                srdelete_state=SReqDeleteState.sreq_selecting
            )
        ),
        
        SReqDeleteState.sreqid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['delete']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.delete,
                    srdelete_state=SReqDeleteState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['delete']["delete_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.delete,
                    srdelete_state=SReqDeleteState.done
                )
            ),
        },
        
        SReqDeleteState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['delete']["stop_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.select_act,
            )
        )
    },

    SReqClarifierState.edit: {
        SReqEditState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["start_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.edit,
                sredit_state=SReqEditState.sreq_selecting
            )
        ),

        SReqEditState.sreq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["select_sr_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.edit,
                sredit_state=SReqEditState.sreq_selecting
            )
        ),

        SReqEditState.sreqid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.edit,
                    sredit_state=SReqEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.edit,
                    sredit_state=SReqEditState.editing_sreq
                )
            ),
        },

        SReqEditState.editing_sreq: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["request_input"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False, 
                user_base_answer=..., # FILLED DYNAMICALLY
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.edit,
                sredit_state=SReqEditState.editing_sreq
            )
        ),

        SReqEditState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["bad_editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.edit,
                    sredit_state=SReqEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SReqClarifierCurrentState(
                    base_state=SReqClarifierState.edit,
                    sredit_state=SReqEditState.done
                )
            ),
        },

        SReqEditState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASREQ_MESSAGE_TAMPLATES['edit']["stop_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SReqClarifierCurrentState(
                base_state=SReqClarifierState.select_act
            )
        ),
    },

    SReqClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BASREQ_MESSAGE_TAMPLATES['stop_sr_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=SReqClarifierCurrentState(
            base_state=SReqClarifierState.done
        )
    ),
}