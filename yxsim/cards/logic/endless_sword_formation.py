from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Endless Sword Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        assert False
