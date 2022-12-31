from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart, OnChangeHealth
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class AshesPhoenixOnChangeHealth(OnChangeHealth):
    def handle(self, **kwargs):
        # TODO is this healing or not???
        print(self.source.health)
        if self.source.health <= 0:
            self.source.health = 10
            Action(
                card=self.source_card,
                source=self.source,
                target=self.source,
                max_hp_change=10
            ).execute()


class CardType(Card):
    display_name = 'Ashes Phoenix'
    phase = 1

    pet = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(AshesPhoenixOnChangeHealth(source=attacker, source_card=self))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 10})
        card_user.health = 3
        combat(card_user, opponent, limit=2)
        assert card_user.health == 10
        assert card_user.max_health == 20
