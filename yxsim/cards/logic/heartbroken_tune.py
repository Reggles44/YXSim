from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class HeartBrokenTuneOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=attacker,
            resource_changes={Resource.INTERNAL_INJURY: 1}
        ).execute()


class CardType(Card):
    display_name = 'Carefree Tune'
    phase = 1

    job = Job.MUSICIAN
    continuous = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        heartbroken_tune_listener = HeartBrokenTuneOnTurnStart(source=attacker, source_card=self, priority=0)
        attacker.add_listener(heartbroken_tune_listener)
        defender.add_listener(heartbroken_tune_listener)
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        print(card_user.resources, opponent.resources)
        assert card_user.resources[Resource.INTERNAL_INJURY] == 1
        assert opponent.resources[Resource.INTERNAL_INJURY] == 1