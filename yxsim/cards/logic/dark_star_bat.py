from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart, OnAttack
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class DarkStarBatOnAttack(OnAttack):
    def handle(self, action: Action, **kwargs):
        if action.damage_to_health <= 5:
            Action(
                card=self.source_card,
                source=self.source,
                target=self.source,
                healing=action.damage_to_health
            ).execute()


class CardType(Card):
    display_name = 'Dark Star Bat'
    phase = 1

    pet = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(DarkStarBatOnAttack(source=attacker, source_card=self))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health
