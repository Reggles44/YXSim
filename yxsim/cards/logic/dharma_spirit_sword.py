from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Cloud Sword Hexagram'
    phase = 3
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda source: 5+5*source.resources[Resource.QI])),
                Action(card=self, source=attacker, target=attacker, resource_exhaust=ReferenceValue(lambda source: {Resource.QI: source.resources[Resource.QI]})),
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 10
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 0
        assert opponent.health == opponent.max_health - 55