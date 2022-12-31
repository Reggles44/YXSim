from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Escape Plan'
    phase = 4
    sect = Sect.HEPTASTAR
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.DEF: 9},
            healing=9,
            post_action=Action(card=self, source=attacker, target=attacker, resource_changes={Resource.GUARD_UP: 1})
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'health': 50, 'max_health': 100})
        combat(card_user, opponent, limit=1)
        assert card_user.health == 59
        assert card_user.resources[Resource.DEF] == 9

    def test_card_twice(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.PLAY_TWICE] = 1
        combat(card_user, opponent, limit=1)
        assert card_user.health == 68
        assert card_user.resources[Resource.DEF] == 18
        assert card_user.resources[Resource.GUARD_UP] == 1
