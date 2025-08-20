from enum import Enum

class ScenariosClarifierState(Enum):
    greetings: int = 0
    fixing_userstory: int = 1
    clarifying_scenario: int = 2
    done: int = 3