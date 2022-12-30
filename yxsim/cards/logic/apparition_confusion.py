from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnStart, OnTurnEnd, OnAttack
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class ApparitionConfusionOnAttack(OnAttack):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        return Action(
            card=self.source_card,
            source=self.source,
            target=attacker,
            damage=3,
            ignore_armor=True
        ).execute()


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
        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=9)
        assert card_user.health == card_user.max_health - 24
        assert opponent.health == opponent.max_health - 24


    def test_card_multiattack(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'tri_peak_sword']})
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health - 12
