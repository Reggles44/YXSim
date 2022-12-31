from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.util import RandomValue
import typing


class CardType(Card):
    display_name = 'Flame Hexagram'
    phase = 4
    sect = Sect.CLOUD
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.HEXAGRAM: 3}),
                Action(card=self, source=attacker, target=defender, max_hp_change=-2)
            ],
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        max_health = opponent.max_health
        health = opponent.health
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == max_health - 2
        assert card_user.resources[Resource.HEXAGRAM] == 3
        assert opponent.health == opponent.max_health

