from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum
from random import shuffle, choice


class MoveType(Enum):
    PUT = "put"
    BEAT = "beat"
    TAKE = "take"
    BITO = "bito"
    REVERSE = "reverse"

@dataclass
class MoveAction:
    move_type: MoveType
    cards: Optional[List[str]] = None
    place: Optional[int] = None


class MoveValidator:
    def __init__(self, trump_suit: str, standard_cards: List[str]):
        self.trump_suit = trump_suit
        self.standard_cards = standard_cards

    def check_put(self, card: str, table: List[List[str]]) -> bool:
        if card not in self.standard_cards:
            return False
        if not table:
            return True
        if len(table) >= 6:
            return False
        return any(card[:-1] == c[:-1] for pair in table for c in pair)

    def check_beat(self, card: str, table: List[List[str]], place: Optional[int]) -> Tuple[bool, Optional[int]]:
        if card not in self.standard_cards:
            return False, None
        if place is None:
            for i, pair in enumerate(table):
                if len(pair) == 1:
                    place = i
                    break
        if place is not None and len(table[place]) == 1:
            if (table[place][0][-1] == card[-1] or card[-1] == self.trump_suit or card[-1] in ['r', 'b']) and \
               self.higher_card(card, table[place][0]):
                return True, place
        return False, None

    def higher_card(self, higher_card: str, card: str) -> bool:
        # Логика сравнения карт (как в методе higher_card из предыдущего кода)
        pass

    def check_reverse(self, card: str, table: List[List[str]]) -> bool:
        for pair in table:
            if len(pair) == 2:
                break
            if card[:-1] == pair[0][:-1]:
                return True
        return False