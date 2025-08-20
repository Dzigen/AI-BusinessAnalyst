from dataclasses import dataclass, field
from typing import Dict, List, Union, Set

@dataclass
class UserStory:
    id: str
    statement: str
    related_scenario_ids: List[str] = field(default_factory=lambda: list())

@dataclass
class Scenario:
    id: str
    statement: str = None
    title: Union[None, str] = None
    steps: List[str] = field(default_factory=lambda: list())
    related_userstory_ids: List[str] = field(default_factory=lambda: list())

    def formate_to_str(self):
        formated_title = f"Сценарий: {self.title} (СИ# {self.id})"
        formated_steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(self.steps)])
        return f"{formated_title}\n{formated_steps}"

@dataclass
class Role:
    id: str
    name: str
    description: Union[str, None] = None
    related_userstory_ids: Set[str] = field(default_factory=lambda: set())
    related_scenarios_ids: Set[str] = field(default_factory=lambda: set())
    
@dataclass
class SystemRequirement:
    id: str
    statement: str
    related_srestr_ids: Set[str] = field(default_factory=lambda: set())
    related_userstory_ids: Set[str] = field(default_factory=lambda: set())
    related_scenarios_ids: Set[str] = field(default_factory=lambda: set())

@dataclass
class SystemRestriction:
    id: str
    statement: str
    related_sreq_ids: Set[str] = field(default_factory=lambda: set())
    related_userstory_ids: Set[str] = field(default_factory=lambda: set())
    related_scenarios_ids: Set[str] = field(default_factory=lambda: set())


@dataclass
class SystemInfo:
    requirements: Dict[str, SystemRequirement] = field(default_factory=lambda: dict())
    restrictions: Dict[str, SystemRestriction] = field(default_factory=lambda: dict())

 #Новый класс   
@dataclass
class FunctionalRestriction:
    id: str
    statement: str
    related_userstory_ids: Set[str] = field(default_factory=lambda: set())
    related_scenarios_ids: Set[str] = field(default_factory=lambda: set())
    related_freq_ids: Set[str] = field(default_factory=lambda: set())

@dataclass
class FunctionalRequirement:
    id: str
    statement: str
    related_userstory_ids: Set[str] = field(default_factory=lambda: set())
    related_scenarios_ids: Set[str] = field(default_factory=lambda: set())
    related_frestr_ids: Set[str] = field(default_factory=lambda: set())
 
@dataclass
class NonFunctionalReuqirement:
    id: str
    statement: str
    related_funcrequirement_ids: List[str] = field(default_factory=lambda: list())
    related_userstory_ids: List[str] = field(default_factory=lambda: list())
    related_scenarios_ids: List[str] = field(default_factory=lambda: list())

@dataclass
class FunctionalRequirementGroup:
    id: str
    title: str
    grouped_funcreq_ids: Set[str] = field(default_factory=lambda: set())

@dataclass
class RequirementsInfo:
    fgroups: Dict[str, FunctionalRequirementGroup] = field(default_factory=lambda: dict())
    functional: Dict[str, FunctionalRequirement] = field(default_factory=lambda: dict())

    functional_restrictions: Dict[str, FunctionalRestriction] = field(default_factory=lambda: dict())
    non_functional: Dict[str, NonFunctionalReuqirement] = field(default_factory=lambda: dict())

@dataclass
class TaskGeneralInfo:
    goal: Union[None, str] = None 
    sub_tasks: Union[None, str] = None
    integration: Union[None, str] = None

@dataclass
class SpecificationInfo:
    general: TaskGeneralInfo = field(default_factory=lambda: TaskGeneralInfo())
    user_stories: Dict[str, UserStory] = field(default_factory=lambda: dict())
    scenarios: Dict[str, Scenario] = field(default_factory=lambda: dict())
    roles: Dict[str, Role] = field(default_factory=lambda: dict())
    system_info: SystemInfo = field(default_factory=lambda: SystemInfo())
    reqs_info: RequirementsInfo = field(default_factory=lambda: RequirementsInfo())
    edit_count: int = 0 # костыль