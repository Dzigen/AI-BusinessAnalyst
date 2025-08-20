from .utils import ICommCurrentState, ICommState
from ...utils import BAResponse, StateAction, WeakReasonerStatus

ICOMMUNICATOR_MAIN_LOG_PATH = 'log/reasoner/weak/i_communicator/main'

BAIC_MESSAGE_TAMPLATES = {
    'greetings': "Привет! Я ваш AI Бизнес Аналитик.",
    'start_task_specification': "Давайте начнём формировать техническое задание."
}

BAIC_RESPONSE_CONFIG = {
    ICommState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BAIC_MESSAGE_TAMPLATES['greetings'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=ICommCurrentState(
            base_state=ICommState.done,
        )
    ),

    ICommState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BAIC_MESSAGE_TAMPLATES['start_task_specification'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=ICommCurrentState(
            base_state=ICommState.done,
        )
    ),
}