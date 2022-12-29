from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Egret Spirit Sword'
    phase = 4
    sect = Sect.CLOUD
    spirit_sword = True
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=ReferenceValue(lambda source: 5+source.resources[Resource.QI]*2)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 11
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 10
        assert opponent.health == opponent.max_health - 25