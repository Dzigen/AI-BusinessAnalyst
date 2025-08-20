import sys
sys.path.insert(0, "../")

from src.reasoner.utils import DialogueHistory, Response

BPQUESTION_STUB = 'уточняющий вопрос #1'

DIALOGUE_HISTORY1 = DialogueHistory(
    sequence=[
        Response(role='ba', text='base ba question #1'),
        Response(role='user', text='base user answer #1')])

DIALOGUE_HISTORY2 = DialogueHistory(
    sequence=[
        Response(role='ba', text='detail ba question #1'),
        Response(role='user', text='detail user answer #1')])

# agent_stubresps, base_dhistory, detail_dhistory, expected_output, is_error_expected
BPCLRF_TEST_CASES = [
    # 1. пустая base_dhistory
    [[BPQUESTION_STUB], DialogueHistory(), DIALOGUE_HISTORY2, None, True],
    # 2. пустая detail_dhistory
    [[BPQUESTION_STUB], DIALOGUE_HISTORY1, DialogueHistory(), BPQUESTION_STUB, False],
    # 3. непустые base_dhistory и detail_dhistory
    [[BPQUESTION_STUB], DIALOGUE_HISTORY1, DIALOGUE_HISTORY2, BPQUESTION_STUB, False],
]