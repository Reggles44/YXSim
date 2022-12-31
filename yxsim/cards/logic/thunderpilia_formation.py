from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd
from yxsim.player import Player
from yxsim.resources import Sect, Job


class ThunderpiliaFormationOnTurnEnd(OnTurnEnd):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=defender,
            damage=4
        ).execute()


class CardType(Card):
    display_name = 'Thunderpilia Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(ThunderpiliaFormationOnTurnEnd(source=attacker, source_card=self, continuous=2, priority=0))
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        action = card_user.actions[0]
        assert opponent.health == opponent.max_health - 7
