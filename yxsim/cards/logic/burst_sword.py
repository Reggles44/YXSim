from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Burst Sword'
    phase = 3
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=11,
            injured_action=Action(card=self, source=attacker, target=defender, resource_changes={Resource.QI: -1})
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 11
        assert opponent.resources[Resource.QI] == 0

    def test_card_opponent_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        opponent.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 11
        assert opponent.resources[Resource.QI] == 0

    def test_card_opponent_lots_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        opponent.resources[Resource.QI] = 11
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 11
        assert opponent.resources[Resource.QI] == 10
