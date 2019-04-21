""" Class that represents an nth sub. """

from dataclasses import dataclass
from typing import List


@dataclass
class NthSub:
    """ Class that represents an nth sub. """
    tags: List[str]
    sub: str
    number: str
