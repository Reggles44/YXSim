from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Consonance Sword Formation'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        si = attacker.resources.get(Resource.SWORD_INTENT)
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_exhaust={
                Resource.SWORD_INTENT:si,
            },
            resource_changes={
                Resource.QI: si,
                Resource.DEF: 9
            }
        ).execute()

    def test_cards(self):
        return ['sword_slash', self.id]

    def test_limit(self):
        return 3

    def asserts(self, card_user, opponent):
        assert card_user.resources.get(Resource.DEF) == 9
        assert card_user.resources.get(Resource.SWORD_INTENT) == 0
        assert card_user.resources.get(Resource.QI) == 2
