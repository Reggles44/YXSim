from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Dark Crystal Heart Shield'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=3),
                Action(card=self, source=attacker, target=defender, resource_changes={Resource.FLAW: 1}),
                Action(card=self, source=attacker, target=defender, damage=3),
                Action(card=self, source=attacker, target=defender, resource_changes={Resource.FLAW: 1}),
                Action(card=self, source=attacker, target=defender, damage=3),
                Action(card=self, source=attacker, target=defender, resource_changes={Resource.FLAW: 1}),
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 2})
        card_user.health = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 11
