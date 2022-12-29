from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Shifting Stars'
    phase = 1
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=5),
                Action(card=self, source=attacker, target=attacker, star_points=attacker.next_slot(1))
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = []
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 5
        assert card_user.star_slots == [1]
        assert card_user.resources[Resource.QI] == 0

    def test_card_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = [1]
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 5
        assert card_user.star_slots == [1]
        assert card_user.resources[Resource.QI] == 1



