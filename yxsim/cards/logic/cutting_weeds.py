from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.util import RandomValue
import typing


class CardType(Card):
    display_name = 'Cutting Weeds'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=5) for _ in range(2)
            ],
            max_hp_change=RandomValue(-3,-13)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1

        max_health = opponent.max_health
        health = opponent.health
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == max_health - 8
        assert opponent.health == max_health - 10

    def test_card_hex(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1

        card_user.resources[Resource.HEXAGRAM] = 1
        max_health = opponent.max_health
        health = opponent.health
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == max_health - 13
        assert opponent.health == max_health - 13
        assert card_user.resources[Resource.HEXAGRAM] == 0
