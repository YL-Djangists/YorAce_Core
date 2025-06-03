from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum
from random import shuffle, choice

@dataclass
class Player:
    player_id: str
    cards: List[str]
    mode: Optional[str]
    status: str
