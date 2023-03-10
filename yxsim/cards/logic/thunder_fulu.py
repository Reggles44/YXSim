from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Thunder Fulu'
    phase = 1

    job = Job.FULULIST
    consumption = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(card=self, source=attacker, target=defender, damage=RandomValue(4, 12)).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-8

    def test_card_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-12
        assert card_user.resources[Resource.HEXAGRAM] == 0

