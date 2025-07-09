from typing import Optional
from player import Player


class Table:
    def __init__(self, trump: str):
        self.slots = []  # Список пар: [подкинутая_карта, отбивающая_карта или None]
        self.trump = trump

    def add_card(self, card: str, place: Optional[int] = None):
        if place is None:
            self.slots.append([card])
        else:
            self.slots[place].append(card)

    def clear(self):
        self.slots = []

    def need_beat(self) -> bool:
        return any(len(pair) == 1 for pair in self.slots)

    def check_bito(self) -> bool:
        if not self.slots:
            return False
        if len(self.slots) == 6 and all(len(pair) == 2 for pair in self.slots):
            return True
        return all(len(pair) == 2 for pair in self.slots)

    def take_cards(self, player: Player):
        for pair in self.slots:
            for card in pair:
                player.cards.append(card)
        self.slots = []
