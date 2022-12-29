from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CareFreeTuneOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=attacker,
            healing=-3,
            resource_changes={Resource.DEF: -3}
        )



class CardType(Card):
    display_name = 'Illusion Tune'
    phase = 1

    job = Job.MUSICIAN
    continuous = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        care_free_tune_listener = CareFreeTuneOnTurnStart(source=attacker, source_card=self, priority=0)
        attacker.add_listener(care_free_tune_listener)
        defender.add_listener(care_free_tune_listener)
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        print(card_user.health, opponent.health)
        assert card_user.health == card_user.max_health - 3
        assert opponent.health == opponent.max_health - 3