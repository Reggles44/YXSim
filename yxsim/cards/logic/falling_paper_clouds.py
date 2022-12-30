import random

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Falling Paper Clouds'
    phase = 1

    job = Job.PAINTER

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        effects = [
            Action(
                card=self,
                source=attacker,
                target=attacker,
                resource_changes={Resource.DEF: 16}
            ),
            Action(
                card=self,
                source=attacker,
                target=attacker,
                healing=12
            ),
            Action(
                card=self,
                source=attacker,
                target=attacker,
                resource_changes={Resource.GUARD_UP: 1}
            ),
        ]

        return random.choice(effects).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.health -= 12
        combat(card_user, opponent, limit=1)

        assert any([
            card_user.resources[Resource.DEF] == 16,
            card_user.health == card_user.max_health,
            card_user.resources[Resource.GUARD_UP] == 1
        ])
