from .utils import BPClarifierState, BPClarifierCurrentState, BPCAskingState
from ...utils import BAResponse, StateAction, WeakReasonerStatus
from ...config import WBAR_GLOBAL_SIGNALSINFO

BPCLARIFIER_MAIN_LOG_PATH = 'log/reasoner/weak/bp_communicator/main'

BABPC_MESSAGE_TAMPLATES = {
    'start_bp_clarifying': "Начинаю уточнение деталей по предметной области проекта.",
    'questions_limit_reached': "Достигнут лимит по количеству заданных уточняющих вопросов.",
    'stop_bp_clarifying': "Уточнение деталей предметной области завершено."
}

BABPC_RESPONSE_CONFIG = {
    BPClarifierState.init: StateAction(
        ba_response=BAResponse(
            ba_text=BABPC_MESSAGE_TAMPLATES['start_bp_clarifying'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
        stage_newstate=BPClarifierCurrentState(
            base_state=BPClarifierState.clarify
        )
    ),
    BPClarifierState.clarify: {
        BPCAskingState.question_preparing: StateAction(
            ba_response=BAResponse(
                ba_text=..., # FILLED DYNAMICALLY
                is_userinput_locked=False,
                available_global_signals=list(WBAR_GLOBAL_SIGNALSINFO.values())
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_response,
            stage_newstate=BPClarifierCurrentState(
                base_state=BPClarifierState.clarify,
                askq_state=BPCAskingState.question_preparing
            )
        ),

        BPCAskingState.limit_exceeded: StateAction(
            ba_response=BAResponse(
                ba_text=BABPC_MESSAGE_TAMPLATES['questions_limit_reached'],
                is_userinput_locked=True
            ),
            reasoner_newstatus=WeakReasonerStatus.waiting_interaction,
            stage_newstate=BPClarifierCurrentState(
                base_state=BPClarifierState.done,
                askq_state=BPCAskingState.limit_exceeded
            )
        ),
    },
    BPClarifierState.done: StateAction(
        ba_response=BAResponse(
            ba_text=BABPC_MESSAGE_TAMPLATES['stop_bp_clarifying'],
            is_userinput_locked=True
        ),
        reasoner_newstatus=WeakReasonerStatus.done,
        stage_newstate=BPClarifierCurrentState(
            base_state=BPClarifierState.done
        )
    ),
}