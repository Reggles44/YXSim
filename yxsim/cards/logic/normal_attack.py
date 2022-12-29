from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Normal Attack'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=self.damage
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        action = card_user.actions[0]
        assert isinstance(action, Action)
        assert action.card.id == self.id
        assert action.source == card_user
        assert action.target == opponent
        assert action.damage == 3
        assert action.executed is True
        assert action.success is True
        assert opponent.health == opponent.max_health - 3
