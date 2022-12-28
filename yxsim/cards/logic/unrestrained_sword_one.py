from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Unrestrained Sword - One'
    phase = 2
    sect = Sect.CLOUD
    unrestrained_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5 + attacker.resources[Resource.UNRESTRAINED_SWORD_COUNTER]*2,
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data()
        combat(p1, p2, limit=5)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user: Player, opponent: Player):
        assert opponent.health == opponent.max_health - 15

    def generate_test_data(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        player_kwargs = player_kwargs or {'cards': ['normal_attack', self.id, self.id]}
        enemy_kwargs = enemy_kwargs or {'cards': []}
        p1 = Player(id="PLAYER", **player_kwargs)
        p2 = Player(id='ENEMY', **enemy_kwargs)
        return p1, p2
