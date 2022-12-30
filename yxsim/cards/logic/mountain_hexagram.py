from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Mountain Hexagram'
    phase = 2
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            max_hp_change=2,
            healing=2,
            resource_changes={Resource.HEXAGRAM: 2}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        max_health = card_user.max_health
        health = card_user.health
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.HEXAGRAM] == 2
        assert card_user.health == card_user.max_health
        assert card_user.max_health == max_health + 2



