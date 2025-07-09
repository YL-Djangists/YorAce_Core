from typing import List, Optional
from deck import Deck
from table import Table
from player import Player
from move import MoveValidator, MoveType, MoveAction


class Fool:
    def __init__(self, player_ids: List[str]):
        self.deck = Deck()
        self.table = Table(self.deck.trump)
        self.players = [
            Player(player_id=pid, cards=[], mode="throws" if i == 0 else "beats" if i == 1 else None, status="active")
            for i, pid in enumerate(player_ids)
        ]
        if not (2 <= len(self.players) <= 9):
            raise ValueError("Only 2 to 9 players allowed")
        self.validator = MoveValidator(self.deck.trump_suit, self.deck.standard_cards)
        self.deck.deal_cards(self.players)

    def move(self, player_id: str, move_action: MoveAction) -> Optional[str]:
        player = next((p for p in self.players if p.player_id == player_id), None)
        if not player:
            raise ValueError(f"Player {player_id} not found")

        if move_action.move_type == MoveType.BITO:
            if player.mode in ['throws', None]:
                player.status = 'bito'
                if self.table.check_bito() and all(p.status == 'bito' for p in self.players if p.mode in ['throws', None]):
                    self.table.clear()
                    self.deck.deal_cards(self.players)
                    for p in self.players:
                        p.status = 'active'
                    return 'bito'
                return None
        elif move_action.move_type == MoveType.TAKE:
            if player.mode == 'beats':
                self.table.take_cards(player)
                self.deck.deal_cards(self.players)
                self.rotate_roles()
                for p in self.players:
                    p.status = 'active'
                return 'take'
            return None
        elif move_action.move_type == MoveType.PUT:
            if player.mode in ['throws', None] and player.status != 'bito':
                for card in move_action.cards or []:
                    if card in player.cards and self.validator.check_put(card, self.table.slots):
                        self.table.add_card(card)
                        player.cards.remove(card)
                    else:
                        return None
            return None
        elif move_action.move_type == MoveType.BEAT:
            if player.mode == 'beats':
                if move_action.cards and len(move_action.cards) == 1:
                    card = move_action.cards[0]
                    if card in player.cards:
                        valid, place = self.validator.check_beat(card, self.table.slots, move_action.place)
                        if valid:
                            self.table.add_card(card, place)
                            player.cards.remove(card)
                        else:
                            return None
            return None
        elif move_action.move_type == MoveType.REVERSE:
            if move_action.cards and len(move_action.cards) == 1 and self.validator.check_reverse(move_action.cards[0], self.table.slots):
                self.table.add_card(move_action.cards[0])
                player.cards.remove(move_action.cards[0])
                self.rotate_roles()
                return 'reverse'
            return None
        return None

    def rotate_roles(self):
        beats_index = next(i for i, p in enumerate(self.players) if p.mode == 'beats')
        self.players[beats_index].mode = 'throws'
        if beats_index == 0:
            self.players[-1].mode = None
            self.players[beats_index + 1].mode = 'beats'
        elif beats_index == len(self.players) - 1:
            self.players[beats_index - 1].mode = None
            self.players[0].mode = 'beats'
        else:
            self.players[beats_index - 1].mode = None
            self.players[beats_index + 1].mode = 'beats'
        for p in self.players:
            p.status = 'active'

    def win(self, player_id: str) -> bool:
        player = next((p for p in self.players if p.player_id == player_id), None)
        return len(self.deck.cards) == 0 and len(player.cards) == 0 if player else False

    def get_game_state(self) -> dict:
        return {
            "table": self.table.slots,
            "trump": self.deck.trump,
            "cards_left": self.deck.cards_left(),
            "players": {p.player_id: {"cards": p.cards, "mode": p.mode, "status": p.status} for p in self.players}
        }
