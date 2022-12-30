import random

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Splash Ink'
    phase = 1

    job = Job.PAINTER

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            resource_changes={random.choice(Resource.debuffs()): 2}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert any(opponent.resources[debuff] == 2 for debuff in Resource.debuffs())
