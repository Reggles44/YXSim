from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class FatImmortalRaccoonOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(
            card=self.source_card,
            source=self.source,
            target=self.source,
            healing=1
        ).execute()


class CardType(Card):
    display_name = 'Fat Immortal Raccoon'
    phase = 1

    pet = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(FatImmortalRaccoonOnTurnStart(source=attacker, source_card=self, priority=0))
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            healing=4
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(enemy_kwargs={'cultivation': 999})
        combat(card_user, opponent, limit=6)
        assert card_user.health == card_user.max_health - 4, card_user.health
