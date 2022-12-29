from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Craze Dance Tune'
    phase = 1

    job = Job.MUSICIAN

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=target,
                    resource_changes={Resource.INCREASE_ATTACK: 2}
                ) for target in [attacker, defender]
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health - 5
        assert opponent.health == opponent.max_health - 5