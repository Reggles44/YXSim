from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Thunder Fulu'
    phase = 1

    job = Job.FULULIST
    consumtion = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        return Action(card=self, source=attacker, target=defender, damage=RandomValue(4, 12)).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-8
