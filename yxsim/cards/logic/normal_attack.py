from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Normal Attack'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(card_id=self.id, source=attacker, target=defender, damage=3).execute()

    def asserts(self, card_user, opponent):
        action = card_user.actions[0]
        assert isinstance(action, Action)
        assert action.card_id == self.id
        assert action.source == card_user
        assert action.target == opponent
        assert action.damage == 3
        assert action.executed is True
        assert action.success is True
        assert action.nested is False