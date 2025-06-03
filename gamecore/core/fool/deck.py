from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum
from random import shuffle, choice


class Deck:
    def __init__(self):
        self.cards = [f"{i}{s}" for i in list(range(2, 11)) + ['J', 'Q', 'K', 'A'] for s in ['s', 'd', 'h', 'c']]
        self.cards.extend(['JOKb', 'JOKr'])
        self.standard_cards = self.cards.copy()
        self.trump = choice(self.cards)
        while self.trump in ['JOKb', 'JOKr']:
            self.trump = choice(self.cards)
        self.cards.remove(self.trump)
        shuffle(self.cards)
        self.cards.append(self.trump)
        self.trump_suit = self.trump[-1]

    def deal_cards(self, players: List[Player], num_cards: int = 6):
        for player in players:
            for _ in range(num_cards - len(player.cards)):
                if not self.cards:
                    break
                player.cards.append(self.cards.pop(0))
            player.cards = self.sort_cards(player.cards)

    def sort_cards(self, cards: List[str]) -> List[str]:
        # Логика сортировки карт (как в методе sort из предыдущего кода)
        pass

    def cards_left(self) -> int:
        return len(self.cards)
