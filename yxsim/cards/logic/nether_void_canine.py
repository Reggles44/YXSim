from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart, OnPrePlayCard
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.cards.logic import registry as card_registry


class NetherVoidCanineOnPrePlayCard(OnPrePlayCard):
    def handle(self, attacker: Player, card: Card, **kwargs):
        attacker.cards[attacker.cards.index(card)] = card_registry['normal_attack']


class CardType(Card):
    display_name = 'Nether Void Canine'
    phase = 1

    pet = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        defender.add_listener(NetherVoidCanineOnPrePlayCard(source=attacker, source_card=self))
        return Action(
            card=self,
            source=attacker,
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(enemy_kwargs={'cards': ['guard_qi']})
        combat(card_user, opponent, limit=2)
        assert opponent.cards[0].display_name == 'Normal Attack'
