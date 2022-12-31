from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Anthomania Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.BLACK_TURTLE: 1, Resource.DEF: 4}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.DEF] == 4
        assert card_user.resources[Resource.BLACK_TURTLE] == 1
