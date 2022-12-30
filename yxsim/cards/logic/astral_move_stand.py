from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Astral Move - Stand'
    phase = 2
    sect = Sect.HEPTASTAR
    qi = 0
    astral_move = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=7,
            star_point_action=Action(card=self, source=attacker, target=attacker, resource_changes={Resource.QI: 1})
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 7
        assert card_user.resources[Resource.QI] == 1


    def test_card_slot(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = [0]
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 7
        assert card_user.resources[Resource.QI] == 2
