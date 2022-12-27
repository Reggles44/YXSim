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

    def play(self, **kwargs) -> bool:
        raise NotImplementedError

    def test(self, *players):
        p1, p2 = self.generate_test_data()
        combat(p1, p2, limit=1)
        self.asserts(p1, p2)

    def generate_test_data(self) -> typing.Tuple['Player', 'Player']:
        return Player(id='PLAYER', cards=[self.id]), Player(id='ENEMY', cards=[])

    def asserts(self, card_user, opponent):
        raise NotImplementedError
