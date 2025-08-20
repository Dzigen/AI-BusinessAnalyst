from collections import deque
from typing import List

from ..utils import AbstractAgentConnector, AgentConnectorConfig

DEFAULT_STUBAGENT_CONFIG = AgentConnectorConfig(ext_params={'stub_answers': []})

class StubAgentConnector(AbstractAgentConnector):
    def __init__(self, config: AgentConnectorConfig = DEFAULT_STUBAGENT_CONFIG) -> None:
        self.config = config
        self.looped_answers = deque(self.config.ext_params['stub_answers'])

    def check_connection(self) -> bool:
        return True

    def close_connection(self):
        pass

    def generate(self, system_prompt: str, user_prompt: str, assistant_prompt: str = None) -> str:
        answer = ''
        if len(self.looped_answers):
            answer = self.looped_answers.popleft()
            self.looped_answers.append(answer)
        return answer
