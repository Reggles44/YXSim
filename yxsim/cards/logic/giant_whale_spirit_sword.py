from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
import typing

class CardType(Card):
    display_name = 'Giant Whale Spirit Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 2
    spirit_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=16
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 2
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 16
