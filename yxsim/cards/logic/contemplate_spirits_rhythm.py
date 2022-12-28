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
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': ['sword_slash', self.id]})
        combat(card_user, opponent, limit=3)
        assert card_user.resources.get(Resource.DEF) == 9
        assert card_user.resources.get(Resource.SWORD_INTENT) == 0
        assert card_user.resources.get(Resource.QI) == 2
