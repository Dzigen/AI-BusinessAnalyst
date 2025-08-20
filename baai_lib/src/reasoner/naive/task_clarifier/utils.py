from enum import Enum

class TaskClarifierState(Enum):
    greetings: int = 0
    clarifying: int = 1
    done: int = 2