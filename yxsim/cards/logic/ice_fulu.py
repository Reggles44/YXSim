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
                Action(card=self, source=attacker, target=defender, damage=4, ignore_armor=True) for _ in range(2)
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.DEF] = 1000
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 8
