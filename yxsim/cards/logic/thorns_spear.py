from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Thorns Spear'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=ReferenceValue(lambda target: (target.resource[Resource.DEF]//2) + 10)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.DEF] = 4
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 8
