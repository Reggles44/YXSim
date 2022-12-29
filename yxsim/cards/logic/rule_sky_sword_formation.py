from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue

class CardType(Card):
    display_name = 'Rule Sky Sword Formation'
    phase = 5
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            chase=True,
            resource_changes={Resource.DEF: 6},
            free=ReferenceValue(lambda source: source.resources[Resource.DEF] > 0)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.DEF] == 6
        assert card_user.resources[Resource.QI] == 0
        assert opponent.health == opponent.max_health - 3

    def test_card_works(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        card_user.resources[Resource.DEF] = 10
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.DEF] == 11
        assert card_user.resources[Resource.QI] == 1
        assert opponent.health == opponent.max_health - 3