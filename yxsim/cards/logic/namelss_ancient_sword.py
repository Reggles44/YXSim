from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Nameless Ancient Sword'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=11 + (11 if attacker.health < 12 else 0)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.health = 11
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 22
