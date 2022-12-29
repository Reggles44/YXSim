from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Great Recovery Elixir'
    phase = 1

    job = Job.ELIXIRIST
    consumption = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            max_hp_change=13,
            healing=13
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 1})
        combat(card_user, opponent, limit=1)
        assert card_user.health == card_user.max_health == 14
