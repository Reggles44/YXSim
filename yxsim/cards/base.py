import typing
import inspect
from copy import deepcopy

from yxsim.combat import combat
from yxsim.player import Player


class Card:
    id = ''
    display_name = ''

    # TODO Add all possible card attributes
    exhausted = False
    continuous = False
    cloud_sword = False
    unrestrained_sword = False
    qi = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.display_name

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        raise NotImplementedError

    def test(self):
        [func() for name, func in inspect.getmembers(self, predicate=inspect.ismethod) if name.startswith('test_')]

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert False

    def generate_test_data(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        return Player(id="PLAYER", **({'cultivation': 100, 'cards': [self.id]} | (player_kwargs or {}))), \
            Player(id='ENEMY', **({'cards': []} | (enemy_kwargs or {})))
