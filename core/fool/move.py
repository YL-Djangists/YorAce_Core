from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


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
        if card not in ['JOKr', 'JOKb']:
            card = card.replace("J", '11')
            card = card.replace("Q", '12')
            card = card.replace("K", '13')
            card = card.replace("A", '14')
        if higher_card not in ['JOKr', 'JOKb']:
            higher_card = higher_card.replace("J", '11')
            higher_card = higher_card.replace("Q", '12')
            higher_card = higher_card.replace("K", '13')
            higher_card = higher_card.replace("A", '14')
        if higher_card[-1] == self.trump_suit:
            if card[-1] == self.trump_suit:
                return int(higher_card[:-1]) > int(card[:-1])
            elif card in ['JOKr', 'JOKb']:
                if self.trump_suit in ['h', 'd']:
                    if card == 'JOKr':
                        return False
                    else:
                        return True
                else:
                    if card == 'JOKb':
                        return False
                    else:
                        return True
            else:
                return True
        elif higher_card in ['JOKr', 'JOKb']:
            if card[-1] == self.trump_suit:
                if self.trump_suit in ['h', 'd']:
                    if higher_card == 'JOKr':
                        return True
                    else:
                        return False
                else:
                    if higher_card == 'JOKb':
                        return True
                    else:
                        return False
            return True
        else:
            if card[-1] == self.trump_suit:
                return False
            else:
                if higher_card[-1] == card[-1]:
                    return int(higher_card[:-1]) > int(card[:-1])
                else:
                    return False

    def check_reverse(self, card: str, table: List[List[str]]) -> bool:
        for pair in table:
            if len(pair) == 2:
                break
            if card[:-1] == pair[0][:-1]:
                return True
        return False