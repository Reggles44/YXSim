import random

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import ReferenceValue, has_debuffs


class CardType(Card):
    display_name = 'Ruthless Water'
    phase = 3
    qi = 1

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:

        return Action(
            card=self,
            source=attacker,
            target=attacker,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=defender,
                    damage=6
                ),
                Action(
                    card=self,
                    source=attacker,
                    target=defender,
                    resource_changes=ReferenceValue(lambda target: {Resource.INTERNAL_INJURY: 2} if has_debuffs(target) else None)
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.WEAKENED] = 3
        card_user.resources[Resource.QI]  = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert opponent.resources[Resource.INTERNAL_INJURY] == 2

    def test_card_injury(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.INTERNAL_INJURY] = 3
        card_user.resources[Resource.QI]  = 1

        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert opponent.resources[Resource.INTERNAL_INJURY] == 5

    def test_card_off(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI]  = 1

        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert opponent.resources[Resource.INTERNAL_INJURY] == 0