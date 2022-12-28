from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Consonance Sword Formation'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        sword_intent = attacker.resources[Resource.SWORD_INTENT]
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_exhaust={
                Resource.SWORD_INTENT: sword_intent,
            },
            resource_changes={
                Resource.QI: sword_intent,
                Resource.DEF: 9
            }
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data(player_kwargs={'cards': ['sword_slash', self.id]})
        combat(p1, p2, limit=3)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user, opponent):
        assert card_user.resources.get(Resource.DEF) == 9
        assert card_user.resources.get(Resource.SWORD_INTENT) == 0
        assert card_user.resources.get(Resource.QI) == 2
