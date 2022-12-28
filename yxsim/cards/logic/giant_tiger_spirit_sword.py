from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
import typing

class CardType(Card):
    display_name = 'Giant Tiger Spirit Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(card=self, source=attacker, target=defender, damage=10).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 10
