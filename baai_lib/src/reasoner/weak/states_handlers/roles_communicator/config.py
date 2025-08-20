from .utils import RExtractorState, RExtractorCurrentState
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...utils import WeakStateSignal

RCOMMUNICATOR_MAIN_LOG_PATH = 'log/reasoner/weak/r_communicator/main'

BARC_MESSAGE_TAMPLATES = {
    'start_rextraction': "Начинаю извлечение ролей из пользовательских историй.",
    'extraction_results': "Извлечение завершено. Обнаружено ролей: {r_amount}.",
    'stop_rextraction': "Операция по извлечению ролей завершена."
}

BARE_RESPONSE_CONFIG = {
    RExtractorState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BARC_MESSAGE_TAMPLATES['start_rextraction'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=RExtractorCurrentState(
            base_state=RExtractorState.extracting_result
        )
    ),
    RExtractorState.extracting_result: StateAction(
        ba_response=BAResponse(
            ba_text=BARC_MESSAGE_TAMPLATES['extraction_results'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=RExtractorCurrentState(
            base_state=RExtractorState.done
        )
    ),
    RExtractorState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BARC_MESSAGE_TAMPLATES['stop_rextraction'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=RExtractorCurrentState(
            base_state=RExtractorState.done
        )
    )
}