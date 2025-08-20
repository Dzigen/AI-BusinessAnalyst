from .utils import SRestrAddState, SRestrClarifierCurrentState, SRestrClarifierState, \
    SRestrDeleteState, SRestrEditState, SRestrRecommendState
from ....utils import SignalInfo
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...utils import WeakStateSignal
from ...config import WBAR_GLOBAL_SIGNALSINFO

SRESRCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/weak/srestr_communicator/main'

BASRESTRCLRF_MESSAGE_TAMPLATES = {
    'start_srs_clarify': "Приступаю к добавлению системных ограничений", 
 #   "selecting_sr": "Пожалуйста, введите идентификатор системного требования.",
 #   'bad_sr_id': "Не удалось найти системное требование.",
 #   'good_sr_id': "Системное требование успешно выбрано.",
    'select_srs_edit_notice': "Вы можете, при необходимости, добавить, удалить, отредактировать системное ограничение или получить рекомендацию ограничения.",
    
    'add': {
        'start_add': "Запускаю операцию добавления системного ограничения.", 
        "selecting_sreq": "Пожалуйста, введите идентификатор системного требования, к которому будет относиться новое ограничение.",
        'bad_sreq_id': "Не удалось найти системное требование.",
        'good_sreq_id': "Системное требование успешно выбрано.",
        'request_input': "Пожалуйста, введите новое системное ограничение.", 
        'bad_input_notice': "Не удалось добавить системное ограничение.", 
        'add_notice': "Системное ограничение успешно добавлено.", 
        'stop_add': "Операция по добавлению нового системного ограничения завершена.", 
    },
    'delete': {
        "start_delete": "Запускаю операцию удаления системного ограничения.", 
        "select_srs_notice": "Пожалуйста, введите идентификатор системного ограничения, которое необходимо удалить.", 
        "bad_select_notice": "Не удалось выбрать системное ограничение.", 
        "delete_notice": "Системное ограничение успешно удалено.", 
        "stop_delete": "Операция по удалению системного ограничения завершена.", 
    },
    'edit': {
        "start_edit": "Запускаю операцию редактирования системного ограничения.", 
        "select_srs_notice": "Пожалуйста, введите идентификатор системного ограничения, которое необходимо отредактировать.", 
        "bad_select_notice": "Не удалось выбрать системное ограничение.", 
        "request_input": "Введите новую формулировку системного ограничения.", 
        "bad_editing_notice": "Не удалось сохраненить изменения.", 
        "editing_notice": "Изменения успешно сохранены.", 
        "stop_edit": "Операция по редактированию системного ограничения завершена.", 
    },
    'recommend': {
        'start_recom': "Начинаю автоматическое формирование возможного/релевантного ограничения.",
        "limit_exceeds": "Достигнут лимит по количеству рекомендуемых ограничений.",
        "selecting_sreq": "Пожалуйста, введите идентификатор системного требования, на основе которой будет предложено ограничение.",
        'chose_note': "Примите решение по предложенному ограничению: добавить его в ТЗ или отклонить: \n{rec_srestr}.",
        'bad_sreq_id': "Не удалось найти системное требование.",
        'good_sreq_id': "Системное требование успешно выбрано.",
        'recom_add_notice': "Рекомендованное системное ограничение успешно добавлено в ТЗ.",
        'stop_recom': "Формирование и обработка рекомендации завершены.",
    },
    'stop_srs_clarify': "Добавление системных ограничений завершено."  
}

WUSC_SELECT_STATE_SIGNALSINFO = {
    'create': SignalInfo(
        signal=WeakStateSignal.add,
        shortcut="Добавить ограничение"
    ),
    'delete': SignalInfo(
        signal=WeakStateSignal.delete,
        shortcut="Удалить ограничение"
    ),
    'update': SignalInfo(
        signal=WeakStateSignal.edit,
        shortcut="Изменить ограничение"
    ),
    'recommend': SignalInfo(
        signal=WeakStateSignal.recommend_new,
        shortcut="Получить предложение ограничения"
    )
}

WUSC_CUD_STATE_SIGNALSINFO = {
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

WUSR_RECOM_STATE_SIGNALSINGO = {
    'approve': SignalInfo(
        signal=WeakStateSignal.approve,
        shortcut="Добавить ограничение в ТЗ"
    ),
    'decline': SignalInfo(
        signal=WeakStateSignal.decline,
        shortcut="Отклонить ограничение"
    ),
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}


BASRESTRC_RESPONSE_CONFIG = {
    SRestrClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['start_srs_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=SRestrClarifierCurrentState(
            base_state=SRestrClarifierState.select_act
        )
    ),
    SRestrClarifierState.select_act: StateAction(
        ba_response=BAResponse(
            ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['select_srs_edit_notice'],
            available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values()),
            available_state_signals=list(WUSC_SELECT_STATE_SIGNALSINFO.values()),
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_response,
        stage_newstate=SRestrClarifierCurrentState(
            base_state=SRestrClarifierState.select_act
        )
    ),

    SRestrClarifierState.add: {
        SRestrAddState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['start_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.add,
                sadd_state=SRestrAddState.sreq_selecting
            )
        ),

        SRestrAddState.sreq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['selecting_sreq'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.add,
                sadd_state=SRestrAddState.sreq_selecting
            )
        ),
        
        SRestrAddState.sreqid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['good_sreq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.add,
                    sadd_state=SRestrAddState.adding_srestr
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['bad_sreq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.add,
                    sadd_state=SRestrAddState.done
                )
            ),
        },
        
        SRestrAddState.adding_srestr: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['request_input'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.add,
                sadd_state=SRestrAddState.adding_srestr
            )
        ),
        
        SRestrAddState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['bad_input_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.add,
                    sadd_state=SRestrAddState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['add_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.add,
                    sadd_state=SRestrAddState.done
                )
            )
        },

        SRestrAddState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['add']['stop_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.select_act,
            )
        )
    },

    SRestrClarifierState.delete: {
        SRestrDeleteState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['delete']["start_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.delete,
                srdelete_state=SRestrDeleteState.srestr_selecting
            )
        ),
        SRestrDeleteState.srestr_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['delete']["select_srs_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.delete,
                srdelete_state=SRestrDeleteState.srestr_selecting
            )
        ),
        SRestrDeleteState.srestrid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['delete']["delete_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.delete,
                    srdelete_state=SRestrDeleteState.done
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['delete']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.delete,
                    srdelete_state=SRestrDeleteState.done
                )
            ),
        },
        SRestrDeleteState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['delete']["stop_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.select_act
            )
        )
    },

    SRestrClarifierState.edit: {
        SRestrEditState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["start_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.edit,
                sedit_state=SRestrEditState.srestr_selecting
            )
        ),

        SRestrEditState.srestr_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["select_srs_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.edit,
                sedit_state=SRestrEditState.srestr_selecting
            )
        ),

        SRestrEditState.srestrid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.edit,
                    sedit_state=SRestrEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.edit,
                    sedit_state=SRestrEditState.editing_srestr
                )
            ),
        },

        SRestrEditState.editing_srestr: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["request_input"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False, 
                user_base_answer=..., # FILLED DYNAMICALLY
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.edit,
                sedit_state=SRestrEditState.editing_srestr
            )
        ),

        SRestrEditState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["bad_editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.edit,
                    sedit_state=SRestrEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.edit,
                    sedit_state=SRestrEditState.done
                )
            ),
        },

        SRestrEditState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['edit']["stop_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.select_act
            )
        ),
    },

    SRestrClarifierState.recommend: {
        SRestrRecommendState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['start_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.recommend,
                srrecomm_state=SRestrRecommendState.sreq_selecting
            )
        ),

        SRestrRecommendState.limit_exceeds: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['limit_exceeds'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.recommend,
                srrecomm_state=SRestrRecommendState.done
            )
        ),

        SRestrRecommendState.sreq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['selecting_sreq'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.recommend,
                srrecomm_state=SRestrRecommendState.sreq_selecting
            )
        ),
        SRestrRecommendState.sreqid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['good_sreq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.recommend,
                    srrecomm_state=SRestrRecommendState.srestr_recommending
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['bad_sreq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SRestrClarifierCurrentState(
                    base_state=SRestrClarifierState.recommend,
                    srrecomm_state=SRestrRecommendState.done
                )
            ),
        },
        SRestrRecommendState.srestr_recommending: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['chose_note'],
                available_state_signals=list(WUSR_RECOM_STATE_SIGNALSINGO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.recommend,
                srrecomm_state=SRestrRecommendState.srestr_recommending
            )
        ),

        SRestrRecommendState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['recommend']['stop_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SRestrClarifierCurrentState(
                base_state=SRestrClarifierState.select_act
            )
        )
    },
    SRestrClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BASRESTRCLRF_MESSAGE_TAMPLATES['stop_srs_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=SRestrClarifierCurrentState(
            base_state=SRestrClarifierState.done
        )
    ),
}