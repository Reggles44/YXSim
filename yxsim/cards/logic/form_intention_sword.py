from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
import typing


class CardType(Card):
    display_name = 'Form-Intention Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card=self,
                source=attacker,
                target=attacker,
                resource_changes={Resource.SWORD_INTENT: 3},
            )
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 8
        assert card_user.resources.get(Resource.SWORD_INTENT) == 3
