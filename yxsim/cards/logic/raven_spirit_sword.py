from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Raven Spirit Sword'
    phase = 3
    sect = Sect.CLOUD
    spirit_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=5),
                Action(card=self, source=attacker, target=attacker, resource_changes=ReferenceValue(lambda source: {Resource.DEF: source.resources[Resource.QI]*2}))
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 0
        assert card_user.resources[Resource.DEF] == 0
        assert opponent.health == opponent.max_health - 5

    def test_card_with_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 10
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 10
        assert card_user.resources[Resource.DEF] == 20
        assert opponent.health == opponent.max_health - 5