from .naive import NaiveBAReasoner
from .weak import WeakBAReasoner

BAREASONER_MAIN_LOG_PATH = ...

AVAILABLE_BA_REASONERS = {
    'naive': NaiveBAReasoner,
    'weak': WeakBAReasoner,
    'medium': ...,
    'string': ...
}