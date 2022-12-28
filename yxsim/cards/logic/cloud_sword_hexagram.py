from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Cloud Sword Hexagram'
    phase = 3
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:

        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.QI: 2}),
                Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda attacker: attacker.resources.get(Resource.QI), attacker=attacker))
            ]
        ).execute()

    def asserts(self, card_user, opponent):
        assert card_user.resources[Resource.QI] == 2
        assert opponent.health == opponent.max_health - 2