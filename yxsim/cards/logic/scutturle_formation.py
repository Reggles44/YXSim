from importlib.resources import Resource

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd
from yxsim.player import Player
from yxsim.resources import Sect, Job


class ScutturtleFormationOnTurnEnd(OnTurnEnd):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=self.source,
            resource_changes={Resource.DEF: 3}
        ).execute()


class CardType(Card):
    display_name = 'Scutturle Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(ScutturtleFormationOnTurnEnd(source=attacker, source_card=self, continuous=4, priority=0))
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=8)
        assert card_user.health == card_user.max_health
