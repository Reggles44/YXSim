import typing
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

    def play(self, **kwargs) -> bool:
        raise NotImplementedError

    def test(self, *players):
        p1, p2 = self.generate_test_data()
        combat(p1, p2, limit=self.test_limit())
        self.asserts(p1, p2)
        return p1, p2

    def test_limit(self):
        return 1

    def test_cards(self):
        return [self.id]

    def generate_test_data(self) -> typing.Tuple['Player', 'Player']:
        return Player(id='PLAYER', cards=self.test_cards()), Player(id='ENEMY', cards=[])

    def asserts(self, card_user, opponent):
        raise NotImplementedError
