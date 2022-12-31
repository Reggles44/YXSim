from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class VoidTheSpiritConsumerOnTurnStart(OnTurnStart):
    def handle(self, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=defender,
            resource_changes={Resource.QI: -1}
        ).execute()


class CardType(Card):
    display_name = 'Void The Spirit Consumer'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(VoidTheSpiritConsumerOnTurnStart(source=attacker, source_card=self))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=3)
        assert opponent.resources[Resource.QI] == 0