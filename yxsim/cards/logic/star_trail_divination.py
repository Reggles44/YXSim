from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Star Trail Divination'
    phase = 4
    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes=ReferenceValue(
                        lambda source: {
                            Resource.DEF: 6,
                            Resource.STAR_POWER: source.resources[Resource.HEXAGRAM],
                            Resource.QI: source.resources[Resource.HEXAGRAM]
                        }
                    )
                ),
                Action(card=self, source=attacker, target=attacker, resource_exhaust=ReferenceValue(lambda source: {Resource.HEXAGRAM: source.resources[Resource.HEXAGRAM]})),
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.HEXAGRAM] = 10
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.QI] == 10
        assert card_user.resources[Resource.STAR_POWER] == 10

    def test_card_none(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.HEXAGRAM] = 0
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.QI] == 0
        assert card_user.resources[Resource.STAR_POWER] == 0