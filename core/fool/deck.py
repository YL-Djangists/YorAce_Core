from typing import List
from random import shuffle, choice
from player import Player


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

    def num(self, x):
       if 'JOK' in x:
           if self.trump in ['h', 'd']:
               if x[-1] == 'r':
                   return 1
               else:
                   return 0
           else:
               if x[-1] == 'b':
                   return 1
               else:
                   return 0
       x = x.replace('J', '11')
       x = x.replace('Q', '12')
       x = x.replace('K', '13')
       x = x.replace('A', '14')
       return int(x[:-1])

    def sort_cards(self, cards: List[str]) -> List[str]:
        s, h, c, d, JOK = [], [], [], [], []
        for i in cards:
            if i[-1] == 's':
                s.append(i)
            elif i[-1] == 'h':
                h.append(i)
            elif i[-1] == 'c':
                c.append(i)
            elif i[-1] == 'd':
                d.append(i)
            elif i[-1] in ['r', 'b']:
                JOK.append(i)
        s.sort(key=self.num)
        h.sort(key=self.num)
        c.sort(key=self.num)
        d.sort(key=self.num)
        JOK.sort(key=self.num)
        if self.trump == 's':
            return h + c + d + s + JOK
        elif self.trump == 'h':
            return s + c + d + h + JOK
        elif self.trump == 'c':
            return s + h + d + c + JOK
        else:
            return s + h + c + d + JOK

    def cards_left(self) -> int:
        return len(self.cards)
