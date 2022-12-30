from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Toning'
    phase = 1

    job = Job.PAINTER

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=2,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes={Resource.QI: 1, Resource.DEF: 3}
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 2
        assert card_user.resources[Resource.QI] == 1
        assert card_user.resources[Resource.DEF] == 3
