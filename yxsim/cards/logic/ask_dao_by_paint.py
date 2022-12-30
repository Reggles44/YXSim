from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Ask Dao By Paint'
    phase = 1

    job = Job.PAINTER

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
        )

    def test_card(self):
        pass
