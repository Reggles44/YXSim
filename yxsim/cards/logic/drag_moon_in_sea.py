from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Drag Moon In Sea'
    phase = 3
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            post_action=Action(card=self, source=attacker, target=defender, chase=True, damage=12)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health

    def test_card_twice(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.PLAY_TWICE] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 15

