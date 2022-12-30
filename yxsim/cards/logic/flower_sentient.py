from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Flower Sentient'
    phase = 2
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.QI: 1, Resource.DEF: 1}),
                Action(card=self, source=attacker, target=defender, resource_changes={Resource.INTERNAL_INJURY: 1})
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        max_health = card_user.max_health
        health = card_user.health
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 1
        assert card_user.resources[Resource.DEF] == 1
        assert opponent.resources[Resource.INTERNAL_INJURY] == 1




