from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.util import random_chance
import typing


class CardType(Card):
    display_name = "White Snake"
    phase = 3
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                *[Action(card=self, source=attacker, target=defender, resource_changes={Resource.FLAW: 1}) for _ in range(random_chance(1, 0.1, attacker))],
                Action(card=self, source=attacker, target=defender, damage=6),
            ]

        ).execute()

    def test_card(self):
        for _ in range(30):
            card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
            combat(card_user, opponent, limit=1)
            assert opponent.health == opponent.max_health-6

    def test_card_hexagram(self):
        for _ in range(30):
            card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
            card_user.resources[Resource.HEXAGRAM] = 1
            combat(card_user, opponent, limit=1)
            assert opponent.health == opponent.max_health-8
            assert card_user.resources[Resource.HEXAGRAM] == 0

