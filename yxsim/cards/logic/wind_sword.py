from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Wind Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(card=self, source=attacker, target=defender, related_actions=[
            Action(card=self, source=attacker, target=defender, damage=3) for _ in range(2)
        ]).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.SWORD_INTENT] = 5
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == opponent.health + 16
        return card_user, opponent

    def test_sword_intent(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, self.id]})
        card_user.resources[Resource.SWORD_INTENT] = 5
        combat(card_user, opponent, limit=3)
        assert opponent.max_health == opponent.health + 16+6
        return card_user, opponent
