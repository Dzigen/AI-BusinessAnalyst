from enum import Enum

class FuncRequirementsExtractorState(Enum):
    greetings: int = 0
    extracting: int = 1
    done: int = 2