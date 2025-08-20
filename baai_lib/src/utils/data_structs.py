from dataclasses import dataclass, field
from typing import List, Union, Tuple, Dict
from enum import Enum
from time import time
import hashlib

def create_id(seed: str = None, id_len: int = 5) -> str:
    if id_len < 1 and id_len > 32:
        raise ValueError
    if seed is None:
        seed = str(time())[::-1]
    return hashlib.md5(seed.encode()).hexdigest()[:id_len]