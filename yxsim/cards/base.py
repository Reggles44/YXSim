import typing
import inspect
from copy import deepcopy

from yxsim.combat import combat
from yxsim.player import Player


class Card:
    id = ''
    display_name = ''

    # TODO Add all possible card attributes
    consume = False
    continuous = False
    cloud_sword = False
    unrestrained_sword = False
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        raise NotImplementedError

    def test(self):
        [func() for name, func in inspect.getmembers(self, predicate=inspect.ismethod) if name.startswith('test_')]

    def test_card(self):
        p1, p2 = self.generate_test_data()
        combat(p1, p2, limit=1)
        self.asserts(p1, p2)
        return p1, p2

    def generate_test_data(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        player_kwargs = player_kwargs or {'cards': [self.id]}
        enemy_kwargs = enemy_kwargs or {'cards': []}
        return Player(id="PLAYER", **player_kwargs), Player(id='ENEMY', **enemy_kwargs)

    def asserts(self, card_user: Player, opponent: Player):
        raise NotImplementedError
