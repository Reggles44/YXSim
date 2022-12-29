from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Concentric Tune'
    phase = 2

    job = Job.ELIXIRIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        pass

    def test_card(self):
        assert False
