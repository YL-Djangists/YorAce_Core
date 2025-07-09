from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Player:
    player_id: str
    cards: List[str]
    mode: Optional[str]
    status: str
