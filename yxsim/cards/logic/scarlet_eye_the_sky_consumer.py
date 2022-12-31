from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class ScarletEyeTheSkyConsumerOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            related_actions=[
                Action(
                    card=self.source_card,
                    source=self.source,
                    target=defender,
                    damage=2,
                    ignore_armor=True
                ),
                Action(
                    card=self.source_card,
                    source=self.source,
                    target=self.source,
                    healing=2
                )
            ]
        ).execute()


class CardType(Card):
    display_name = 'Scarlet-Eye the Sky Consumer'
    phase = 1

    pet = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(ScarletEyeTheSkyConsumerOnTurnStart(source=attacker, source_card=self, priority=0))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health - 1
        assert opponent.health == opponent.max_health - 5
