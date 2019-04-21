from dataclasses import dataclass
from typing import List

# class that represents an nthsub
@dataclass
class NthSub:
    tags: List[str]
    sub: str
    number: str
