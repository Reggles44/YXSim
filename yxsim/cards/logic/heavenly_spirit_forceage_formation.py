from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class HeavenlySpiritForceageFormationOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=self.source,
            resource_changes={Resource.INCREASE_ATTACK: 1}
        ).execute()


class CardType(Card):
    display_name = 'Heavenly Spirit Forceage Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(HeavenlySpiritForceageFormationOnTurnStart(source=attacker, source_card=self, continuous=2, priority=0))
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=5)
        assert card_user.resources[Resource.INCREASE_ATTACK] == 2
        assert opponent.health == opponent.max_health - 9
