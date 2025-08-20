from .utils import WeakGlobalSignal, WeakReasonerState
from ..utils import SignalInfo

WEAKBAREASONER_MAIN_LOG_PATH = 'log/reasoner/weak/main'


WBAR_GLOBAL_SIGNALSINFO = {
    'next_stage': SignalInfo(
        signal=WeakGlobalSignal.next_stage,
        shortcut="Перейти на следующую стадию"
    ),
}