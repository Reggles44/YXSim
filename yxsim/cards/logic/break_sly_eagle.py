from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class BreakSkyEagleOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=defender,
            damage=1
        ).execute()


class CardType(Card):
    display_name = 'Break Sky Eagle'
    phase = 1

    pet = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(BreakSkyEagleOnTurnStart(source=attacker, source_card=self, priority=0))
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=4
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health - 8
