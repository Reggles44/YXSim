from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Spritiage Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        gain_qi = 2
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.QI: gain_qi}),
                *[Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda source: 2 if source.resources[Resource.QI] > 2 else None)) for _ in range(2)]
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources.get(Resource.QI) == 2
        assert opponent.max_health == opponent.health

    def test_much_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert card_user.resources.get(Resource.QI) == 3
        assert opponent.max_health == opponent.health + 4
        return card_user, opponent

    #  TODO test - double qi works when it previously wouldn't trigger