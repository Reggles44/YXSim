from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Guard Spirit Fulu'
    phase = 1

    job = Job.FULULIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, max_hp_change=-4) for _ in range(2)
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(enemy_kwargs={'max_health': 9})
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == 1
