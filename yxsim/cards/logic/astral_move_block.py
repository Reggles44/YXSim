from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Astral Move - Block'
    phase = 1
    sect = Sect.HEPTASTAR
    qi = 0
    astral_move = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=6,
            star_point_action=Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: 2})
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert card_user.resources[Resource.DEF] == 0

    def test_card_slots(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = [0]
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert card_user.resources[Resource.DEF] == 2


