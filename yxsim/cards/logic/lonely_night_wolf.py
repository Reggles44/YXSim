from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart, OnAttack, OnChangeHealth
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class LonelyNightWolfOnChangeHealth(OnChangeHealth):
    def handle(self, **kwargs):
        if self.source.health < self.source.max_health/2:
            Action(
                card=self.source_card,
                source=self.source,
                target=self.source,
                resource_changes={Resource.INCREASE_ATTACK: 4}
            ).execute()
            self.source.remove_listener(self)


class CardType(Card):
    display_name = 'Lonely Night Wolf'
    phase = 1

    pet = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(LonelyNightWolfOnChangeHealth(source=attacker, source_card=self))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 5}, enemy_kwargs={'max_health': 7})
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health - 3
        assert opponent.health == 0
