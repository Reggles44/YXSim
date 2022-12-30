from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Thunder And Lightning (1)'
    phase = 1
    qi = 1

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(card=self, source=attacker, target=defender, damage=RandomValue(6, 16)).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-11

    def test_card_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        card_user.resources[Resource.QI] = 1
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-16
        assert card_user.resources[Resource.HEXAGRAM] == 0

