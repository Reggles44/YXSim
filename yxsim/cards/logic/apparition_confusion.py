from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnStart, OnTurnEnd, OnAttack
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class ApparitionConfusionOnAttack(OnAttack):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=attacker,
            healing=-3
        )


class CardType(Card):
    display_name = 'Apparition Confusion'
    phase = 1

    job = Job.MUSICIAN
    continuous = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        apparition_confusion_listener = ApparitionConfusionOnAttack(source=attacker, source_card=self, priority=0)
        attacker.add_listener(apparition_confusion_listener)
        defender.add_listener(apparition_confusion_listener)
        return Action(card=self, source=attacker)

    def test_card(self):
        # TODO does this proc for *each* attack or just the card being played
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 10}, enemy_kwargs={'max_health': 10})
        combat(card_user, opponent, limit=3)
        assert card_user.health == 4
        assert opponent.health == 4
