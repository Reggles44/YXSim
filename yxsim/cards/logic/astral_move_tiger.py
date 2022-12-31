from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Astral Move - Tiger'
    phase = 4
    sect = Sect.HEPTASTAR
    qi = 0
    astral_move = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=1) for _ in range(3)
            ],
            star_point_action=Action(card=self, source=attacker, target=defender, resource_changes={Resource.WEAKENED: 1})
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 3
        assert opponent.resources[Resource.WEAKENED] == 0

    def test_card_slots(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = [0]
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 3
        assert opponent.resources[Resource.WEAKENED] == 1

