from .utils import NaiveGlobalSignal
from ..utils import SignalInfo

NBAR_GLOBAL_SIGNALSINFO = {
    'next_stage': SignalInfo(
        signal=NaiveGlobalSignal.next_stage,
        shortcut="Следующая стадия"
    )
}