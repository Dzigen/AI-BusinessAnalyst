from .utils import DCommState, DCommCurrentState
from ...utils import BAResponse, StateAction, WeakReasonerStatus, WeakReasonerState

BAD_MESSAGE_TAMPLATES = {
    'exiting_pipeline': "Процесс формирования технического задания завершён."
}

DCOMMUNICATOR_MAIN_LOG_PATH = 'log/reasoner/weak/d_communicator/main'

BADC_RESPONSE_CONFIG = {
     DCommState.notice: StateAction(
          ba_response=BAResponse(
               ba_text=BAD_MESSAGE_TAMPLATES['exiting_pipeline'],
               is_userinput_locked=True
          ),
          stage_newstate=DCommCurrentState(base_state=DCommState.done),
          reasoner_newstatus=WeakReasonerStatus.done,
          reasoner_donestate=WeakReasonerState.done
     )
}