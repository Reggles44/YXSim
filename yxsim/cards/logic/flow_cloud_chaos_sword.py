from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat


class CardType(Card):
    display_name = 'Flow Cloud Chaos Sword'
    phase = 4
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(card=self, source=attacker, target=defender, related_actions=[
            Action(card=self, source=attacker, target=defender, damage=2) for _ in range(4)
        ]).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == opponent.health + 8
        return card_user, opponent
