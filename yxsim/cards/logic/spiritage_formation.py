from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class SpiritageFormationOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=defender,
            resource_changes={Resource.QI: 2}
        ).execute()


class CardType(Card):
    display_name = 'Spiritage Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(SpiritageFormationOnTurnStart(source=attacker, source_card=self, continuous=2, priority=0))
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=5)
        assert card_user.resources[Resource.QI] == 4
