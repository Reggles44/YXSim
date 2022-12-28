from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Normal Attack'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(card=self, source=attacker, target=defender, damage=3).execute()

    def asserts(self, card_user: Player, opponent: Player):
        action = card_user.actions[0]
        assert isinstance(action, Action)
        assert action.card.id == self.id
        assert action.source == card_user
        assert action.target == opponent
        assert action.damage == 3
        assert action.executed is True
        assert action.success is True
        assert opponent.health == opponent.max_health - 3
