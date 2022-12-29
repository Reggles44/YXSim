from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Moon Water Sword Formation'
    phase = 4
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 10,
                Resource.STATIC_DEF: 3
            }
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.DEF] = 180  # immediately halves to 90, then goes to 100
        combat(card_user, opponent, limit=9)
        assert card_user.resources[Resource.DEF] == 44 # 100 - 3*4 //2