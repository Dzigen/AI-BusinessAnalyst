from .utils import FRestrAddState, FRestrClarifierCurrentState, FRestrClarifierState, \
    FRestrDeleteState, FRestrEditState, FRestrRecommendState
from ....utils import SignalInfo
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...utils import WeakStateSignal
from ...config import WBAR_GLOBAL_SIGNALSINFO

FRESRCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/weak/frestr_communicator/main'

BAFRESTRCLRF_MESSAGE_TAMPLATES = {
    'start_frs_clarify': "Приступаю к добавлению функциональных ограничений.", 
    #"selecting_fr": "Пожалуйста, введите идентификатор функционального требования.",
    #'bad_fr_id': "Не удалось найти функциональное требование.",
    #'good_fr_id': "Функциональное требование успешно выбрано.",
    'select_frs_edit_notice': "Вы можете, при необходимости, добавить, удалить, отредактировать или получить рекомендацию функционального ограничения.",
    
    'add': {
        'start_add': "Запускаю операцию добавления функционального ограничения.", 
        "selecting_freq": "Пожалуйста, введите идентификатор функционального требования, к которому будет относиться новое ограничение.",
        'bad_freq_id': "Не удалось найти функциональное требование.",
        'good_freq_id': "Функциональное требование успешно выбрано.",
        'request_input': "Пожалуйста, введите новое функциональное ограничение.", 
        'bad_input_notice': "Не удалось добавить функциональное ограничение.", 
        'add_notice': "Функциональное ограничение успешно добавлено.", 
        'stop_add': "Операция по добавлению нового функционального ограничения завершена.", 
    },
    'delete': {
        "start_delete": "Запускаю операцию удаления функционального ограничения.", 
        "select_notice": "Пожалуйста, введите идентификатор функционального ограничения, которое необходимо удалить.", 
        "bad_select_notice": "Не удалось выбрать функциональное ограничение.", 
        "delete_notice": "Функциональное ограничение успешно удалено.", 
        "stop_delete": "Операция по удалению функционального ограничения завершена.", 
    },
    'edit': {
        "start_edit": "Запускаю операцию редактирования функционального ограничения.", 
        "select_frs_notice": "Пожалуйста, введите идентификатор функционального ограничения, которое необходимо отредактировать.", 
        "bad_select_notice": "Не удалось выбрать функциональное ограничение.", 
        "request_input": "Введите новую формулировку функционального ограничения.", 
        "bad_editing_notice": "Не удалось сохраненить изменения.", 
        "editing_notice": "Изменения успешно сохранены.", 
        "stop_edit": "Операция по редактированию функционального ограничения завершена.", 
    },
    'recommend': {
        'start_recom': "Начинаю автоматическое формирование возможного/релевантного ограничения.",
        "limit_exceeds": "Достигнут лимит по количеству рекомендуемых ограничений.",
        "selecting_freq": "Пожалуйста, введите идентификатор функционального требования, на основе которой будет предложено ограничение.",
        'chose_note': "Примите решение по предложенному ограничению: добавить его в ТЗ или отклонить: \n{rec_frestr}.",
        'bad_freq_id': "Не удалось найти функциональное требование.",
        'good_freq_id': "Функциональное требование успешно выбрано.",
        'recom_add_notice': "Рекомендованное функциональное ограничение успешно добавлено в ТЗ.",
        'stop_recom': "Формирование и обработка рекомендации завершены.",
    },
    'stop_frs_clarify': "Добавление функциональных ограничений завершено."  
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
        shortcut="Получить рекомендацию ограничения"
    )
}

WUSC_CUD_STATE_SIGNALSINFO = {
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

WUFR_RECOM_STATE_SIGNALSINGO = {
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


BAFRESTRC_RESPONSE_CONFIG = {
    FRestrClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['start_frs_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=FRestrClarifierCurrentState(
            base_state=FRestrClarifierState.select_act
        )
    ),
    FRestrClarifierState.select_act: StateAction(
        ba_response=BAResponse(
            ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['select_frs_edit_notice'],
            available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values()),
            available_state_signals=list(WUSC_SELECT_STATE_SIGNALSINFO.values()),
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_response,
        stage_newstate=FRestrClarifierCurrentState(
            base_state=FRestrClarifierState.select_act
        )
    ),

    FRestrClarifierState.add: {
        FRestrAddState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['start_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.add,
                fadd_state=FRestrAddState.freq_selecting
            )
        ),

        FRestrAddState.freq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['selecting_freq'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.add,
                fadd_state=FRestrAddState.freq_selecting
            )
        ),

        FRestrAddState.freqid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['good_freq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.add,
                    fadd_state=FRestrAddState.adding_frestr
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['bad_freq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.add,
                    fadd_state=FRestrAddState.done
                )
            ),
        },
        
        FRestrAddState.adding_frestr: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['request_input'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.add,
                fadd_state=FRestrAddState.adding_frestr
            )
        ),
        
        FRestrAddState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['bad_input_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.add,
                    fadd_state=FRestrAddState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['add_notice'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.add,
                    fadd_state=FRestrAddState.done
                )
            )
        },

        FRestrAddState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['add']['stop_add'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.select_act,
            )
        )
    },

    FRestrClarifierState.delete: {
        FRestrDeleteState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['delete']["start_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.delete,
                frdelete_state=FRestrDeleteState.frestr_selecting
            )
        ),
        FRestrDeleteState.frestr_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['delete']["select_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.delete,
                frdelete_state=FRestrDeleteState.frestr_selecting
            )
        ),
        FRestrDeleteState.frestrid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['delete']["delete_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.delete,
                    frdelete_state=FRestrDeleteState.done
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['delete']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.delete,
                    frdelete_state=FRestrDeleteState.done
                )
            ),
        },
        FRestrDeleteState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['delete']["stop_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.select_act
            )
        )
    },

    FRestrClarifierState.edit: {
        FRestrEditState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["start_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.edit,
                fedit_state=FRestrEditState.frestr_selecting
            )
        ),

        FRestrEditState.frestr_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["select_frs_notice"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.edit,
                fedit_state=FRestrEditState.frestr_selecting
            )
        ),

        FRestrEditState.frestrid_validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.edit,
                    fedit_state=FRestrEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.edit,
                    fedit_state=FRestrEditState.editing_frestr
                )
            ),
        },

        FRestrEditState.editing_frestr: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["request_input"],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False, 
                user_base_answer=..., # FILLED DYNAMICALLY
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.edit,
                fedit_state=FRestrEditState.editing_frestr
            )
        ),

        FRestrEditState.validating: {
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["bad_editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.edit,
                    fedit_state=FRestrEditState.done
                )
            ),
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["editing_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.edit,
                    fedit_state=FRestrEditState.done
                )
            ),
        },

        FRestrEditState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['edit']["stop_edit"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.select_act
            )
        ),
    },

    FRestrClarifierState.recommend: {
        FRestrRecommendState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['start_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.recommend,
                frrecomm_state=FRestrRecommendState.freq_selecting
            )
        ),

        FRestrRecommendState.limit_exceeds: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['limit_exceeds'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.recommend,
                frrecomm_state=FRestrRecommendState.done
            )
        ),

        FRestrRecommendState.freq_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['selecting_freq'],
                available_state_signals=list(WUSC_CUD_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.recommend,
                frrecomm_state=FRestrRecommendState.freq_selecting
            )
        ),

        FRestrRecommendState.freqid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['good_freq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.recommend,
                    frrecomm_state=FRestrRecommendState.frestr_recommending
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['bad_freq_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=FRestrClarifierCurrentState(
                    base_state=FRestrClarifierState.recommend,
                    frrecomm_state=FRestrRecommendState.done
                )
            ),
        },

        FRestrRecommendState.frestr_recommending: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['chose_note'],
                available_state_signals=list(WUFR_RECOM_STATE_SIGNALSINGO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.recommend,
                frrecomm_state=FRestrRecommendState.frestr_recommending
            )
        ),

        FRestrRecommendState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['recommend']['stop_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=FRestrClarifierCurrentState(
                base_state=FRestrClarifierState.select_act
            )
        )
    },
    FRestrClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BAFRESTRCLRF_MESSAGE_TAMPLATES['stop_frs_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=FRestrClarifierCurrentState(
            base_state=FRestrClarifierState.done
        )
    ),
}