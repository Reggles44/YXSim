from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Predicament for Immortals'
    phase = 2

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
                    resource_changes={Resource.CHASE_BLOCKED: 1}
                ) for target in [attacker, defender]
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.CHASE_BLOCKED] == 1
        assert opponent.resources[Resource.CHASE_BLOCKED] == 1

    # TODO Make a proper test for chase blocking
