from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Thunder Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(
                card=self,
                source=attacker,
                target=defender,
                damage=6
            )
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 11

    def test_defense_block(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        opponent.resources[Resource.DEF] = 5
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == opponent.health
        return card_user, opponent

    def test_sword_intent(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        card_user.resources[Resource.SWORD_INTENT] = 5
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == opponent.health + 21
        return card_user, opponent
