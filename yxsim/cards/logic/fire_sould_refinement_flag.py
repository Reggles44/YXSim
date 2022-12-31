from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Fire Soul Refinement Flag'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            healing=-15,
            max_hp_change=-15,
            resource_changes={Resource.INTERNAL_INJURY: 1},
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(enemy_kwargs={'max_health': 16})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health == 1
        assert opponent.resources[Resource.INTERNAL_INJURY] == 1
