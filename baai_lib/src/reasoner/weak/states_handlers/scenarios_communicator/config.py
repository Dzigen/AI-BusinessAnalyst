from .utils import SClarifierCurrentState, SClarifierState, SDeleteState, SRecommendState
from ....utils import SignalInfo
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...utils import WeakStateSignal

SCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/weak/s_communicator/main'

BASC_MESSAGE_TAMPLATES = {
    'start_s_clarify': "Приступаю к уточнению поддерживаемых сценариев.",
    'select_s_edit_notic': "Вы можете, при необходимости удалить или получить рекомендацию сценария.",
#    'add': {
#        'start_add': "Запускаю операцию добавления нового сценария.",
#        'request_input': "Пожалуйста, введите новый сценарий.",
#        'bad_input_notice': "Не удалось добавить сценарий.",
#        'add_notice': "Сценарий успешно добавлен.",
#        'stop_add': "Добавление нового сценария завершено.",
#    },
    'delete': {
        "start_delete": "Запускаю операцию удаления сценария.",
        "select_notice": "Пожалуйста, введите идентификатор сценария, который требуется удалить.",
        "bad_select_notice": "Не удалось найти сценарий.",
        "delete_notice": "Сценарий успешно удалён.",
        "stop_delete": "Удаление сценария завершено.",
    },
#    'edit': {
#        "start_edit": "Запускаю операцию редактирования сценария.",
#        "select_notice": "Пожалуйста, введите идентификатор сценария, который необходимо отредактировать.",
#        "bad_select_notice": "Не удалось найти сценарий.",
#        "request_input": "Введите новую формулировку сценария.",
#        "bad_editing_notice": "Не удалось сохранить изменения.",
#        "editing_notice": "Изменения успешно сохранены.",
#        "stop_edit": "Редактирование сценария завершено.",
#    },
    'recommend': {
        'start_recom': "Начинаю автоматическое формирование рекомендованного сценария.",
        "limit_exceeds": "Достигнут лимит по количеству рекомендуемых сценариев.",
        "selecting_us": "Пожалуйста, введите идентификатор пользовательской истории, на основе которой будет предложен сценарий.",
        'chose_note': "Примите решение по предложенному сценарию: добавить его в ТЗ или отклонить: \n{rec_s}",
        'bad_us_id': "Не удалось найти пользовательскую историю.",
        'good_us_id': "Пользовательская история успешно выбрана.",
        'recom_add_notice': "Рекомендованный сценарий успешно добавлен в ТЗ.",
        'stop_recom': "Формирование и обработка рекомендации завершены.",
    },
    'stop_s_clarify': "Уточнение сценариев завершено."
}

WSC_ADDSCENARIO_STATE_SIGNALINFO = {
    # 'create': SignalInfo(
    #     signal=WeakStateSignal.add,
    #     shortcut="Добавить сценарий"
    # ),
    'delete': SignalInfo(
        signal=WeakStateSignal.delete,
        shortcut="Удалить сценарий"
    ),
    # 'update': SignalInfo(
    #     signal=WeakStateSignal.edit,
    #     shortcut="Изменить сценарий"
    # ),
    'recomend': SignalInfo(
        signal=WeakStateSignal.recommend_new,
        shortcut="Получить предложение сценария"
    ),
    # 'return': SignalInfo(
    #     signal=WeakStateSignal.return_item_operation,
    #     shortcut='Выбрать другую user-историю'
    # )
}

WUSC_CUDR_STATE_SIGNALSINFO = {
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

WUSC_RECOM_STATE_SIGNALSINGO = {
    'approve': SignalInfo(
        signal=WeakStateSignal.approve,
        shortcut="Добавить сценарий в ТЗ"
    ),
    'decline': SignalInfo(
        signal=WeakStateSignal.decline,
        shortcut="Отклонить сценарий"
    ),
    'cancel': SignalInfo(
        signal=WeakStateSignal.cancel_operation,
        shortcut="Отменить действие"
    )
}

BAUSC_RESPONSE_CONFIG = {
    SClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BASC_MESSAGE_TAMPLATES['start_s_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=SClarifierCurrentState(
            base_state=SClarifierState.select_act
        )
    ),
    SClarifierState.select_act: StateAction(
        ba_response=BAResponse(
            ba_text=BASC_MESSAGE_TAMPLATES['select_s_edit_notic'],
            available_global_signals=..., # FILLED DYNAMICALLY
            available_state_signals=list(WSC_ADDSCENARIO_STATE_SIGNALINFO.values()),
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_response,
        stage_newstate=SClarifierCurrentState(
            base_state=SClarifierState.select_act
        )
    ),

    SClarifierState.delete: {
        SDeleteState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['delete']["start_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.delete,
                sdelete_state=SDeleteState.s_selecting
            )
        ),
        SDeleteState.s_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['delete']["select_notice"],
                available_state_signals=list(WUSC_CUDR_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.delete,
                sdelete_state=SDeleteState.s_selecting
            )
        ),
        SDeleteState.sid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASC_MESSAGE_TAMPLATES['delete']["delete_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SClarifierCurrentState(
                    base_state=SClarifierState.delete,
                    sdelete_state=SDeleteState.done
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASC_MESSAGE_TAMPLATES['delete']["bad_select_notice"],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SClarifierCurrentState(
                    base_state=SClarifierState.delete,
                    sdelete_state=SDeleteState.done
                )
            ),
        },
        SDeleteState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['delete']["stop_delete"],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.select_act
            )
        )
    },

    SClarifierState.recommend: {
        SRecommendState.init: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['recommend']['start_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.recommend,
                srecomm_state=... # FILLED DYNAMICALLY
            )
        ),

        SRecommendState.limit_exceeds: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['recommend']['limit_exceeds'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.recommend,
                srecomm_state=SRecommendState.done
            )
        ),
        

        SRecommendState.us_selecting: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['recommend']['selecting_us'],
                available_state_signals=list(WUSC_CUDR_STATE_SIGNALSINFO.values()),
                is_userinput_locked=False
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.recommend,
                srecomm_state=SRecommendState.us_selecting
            )
        ),
        SRecommendState.usid_validating: {
            'good': StateAction(
                ba_response=BAResponse(
                    ba_text=BASC_MESSAGE_TAMPLATES['recommend']['good_us_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SClarifierCurrentState(
                    base_state=SClarifierState.recommend,
                    srecomm_state=SRecommendState.s_recommending
                )
            ),
            'bad': StateAction(
                ba_response=BAResponse(
                    ba_text=BASC_MESSAGE_TAMPLATES['recommend']['bad_us_id'],
                    is_userinput_locked=True
                ),
                reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
                stage_newstate=SClarifierCurrentState(
                    base_state=SClarifierState.recommend,
                    srecomm_state=SRecommendState.done
                )
            ),
        },
        SRecommendState.s_recommending: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['recommend']['chose_note'],
                available_state_signals=list(WUSC_RECOM_STATE_SIGNALSINGO.values()),
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.recommend,
                srecomm_state=SRecommendState.s_recommending
            )
        ),

        SRecommendState.done: StateAction(
            ba_response=BAResponse(
                ba_text=BASC_MESSAGE_TAMPLATES['recommend']['stop_recom'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=SClarifierCurrentState(
                base_state=SClarifierState.select_act
            )
        )
    },
    SClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BASC_MESSAGE_TAMPLATES['stop_s_clarify'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=SClarifierCurrentState(
            base_state=SClarifierState.done
        )
    ),
}