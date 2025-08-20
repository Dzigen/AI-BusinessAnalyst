from .utils import FRExtractorState, FRExtractorCurrentState
from ...utils import BAResponse, StateAction, WeakReasonerStatus

FREQEXTRACTOR_MAIN_LOG_PATH = 'log/reasoner/weak/frestr_communicator/main'
BAFREQ_MESSAGE_TAMPLATES = {
    'start_freq_extraction': "Начинаю извлечение функциональных требований.",
    "funreq_extraction_results": "Извлечение завершено. Обнаружено функциональных требований: {freq_count}.",
    "stop_freq_extraction": "Операция по извлечению функциональных требований завершена."
}

BAFREQC_MESSAGE_TAMPLATES = {
    FRExtractorState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BAFREQ_MESSAGE_TAMPLATES['start_freq_extraction'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=FRExtractorCurrentState(
            base_state=FRExtractorState.extract_results
        )
    ),
    FRExtractorState.extract_results: StateAction(
        ba_response=BAResponse(
            ba_text=BAFREQ_MESSAGE_TAMPLATES["funreq_extraction_results"],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=FRExtractorCurrentState(
            base_state=FRExtractorState.done
        )
    ),
    FRExtractorState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BAFREQ_MESSAGE_TAMPLATES["stop_freq_extraction"],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=FRExtractorCurrentState(
            base_state=FRExtractorState.done
        )
    ),
}