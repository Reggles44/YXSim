from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
import typing

class CardType(Card):
    display_name = 'Giant Whale Spirit Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 2

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=16
        ).execute()

    def generate_test_data(self) -> typing.Tuple[Player, Player]:
        player, enemy = super().generate_test_data()
        player.resources[Resource.QI] = 2
        return player, enemy

    def asserts(self, card_user: Player, opponent: Player):
        assert opponent.health == opponent.max_health - 16
