from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnStart, OnTurnEnd
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class RegenTuneOnTurnEnd(OnTurnEnd):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=attacker,
            max_hp_change=3,
            healing=3
        ).execute()


class CardType(Card):
    display_name = 'Regen Tune'
    phase = 1

    job = Job.MUSICIAN
    continuous = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        regen_tune_listener = RegenTuneOnTurnEnd(source=attacker, source_card=self, priority=0)
        attacker.add_listener(regen_tune_listener)
        defender.add_listener(regen_tune_listener)
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 10}, enemy_kwargs={'max_health': 10})
        combat(card_user, opponent, limit=3)
        assert card_user.health == 13
        assert card_user.max_health == 16
        assert opponent.health == 10
        assert opponent.max_health == 13