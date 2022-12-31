from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Astral Move - Fly'
    phase = 4
    sect = Sect.HEPTASTAR
    qi = 1
    astral_move = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=2) for _ in range(2)
            ],
            star_point_action=Action(card=self, source=attacker, target=defender, chase=True)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 4


    def test_card_slots(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1

        card_user.star_slots = [0]
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 7


