from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Wind Hexagram'
    phase = 1
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.QI: 1, Resource.HEXAGRAM: 1}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 1
        assert card_user.resources[Resource.HEXAGRAM] == 1



