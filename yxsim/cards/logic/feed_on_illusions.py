from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Feed On Illusions'
    phase = 1

    job = Job.PAINTER

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            max_hp_change=10,
            resource_changes={Resource.QI: 2}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 10})
        combat(card_user, opponent, limit=1)
        assert card_user.max_health == 20
        assert card_user.resources[Resource.QI] == 2
