from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect
from yxsim.events import OnInjure


class UnrestrainedSwordZeroOnInjure(OnInjure):
    def handle(self, card: Card, action: Action, attacker: Player, defender: Player, **kwargs):
        if card.unrestrained_sword is True:
            Action(card=self.source_card, source=attacker, target=attacker, healing=(action.damage_to_health*0.3)//1).execute()


class CardType(Card):
    display_name = 'Unrestrained Sword - Zero'
    phase = 5
    unrestrained_sword = True
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        attacker.add_listener(UnrestrainedSwordZeroOnInjure(self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'normal_attack', 'normal_attack', 'unrestrained_sword_two']})
        combat(card_user, opponent, limit=7)

        # TODO Make a real test here
        assert card_user.health == card_user.max_health - 7
