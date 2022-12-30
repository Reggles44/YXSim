from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Imposing'
    phase = 2
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.QI: 2},
            post_action=Action(card=self, source=attacker, target=attacker, healing=6)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'health': 50, 'max_health': 100})
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 2
        assert card_user.health == 50

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'health': 50, 'max_health': 100})
        card_user.resources[Resource.PLAY_TWICE] = 1
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 4
        assert card_user.health == 56

