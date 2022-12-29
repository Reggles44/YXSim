from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Cloud Dance Rhythm'
    phase = 3
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.QI: 2,
                Resource.DEF: 2,
                Resource.SWORD_INTENT: 2
            }
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources.get(Resource.DEF) == 2
        assert card_user.resources.get(Resource.QI) == 2
        assert card_user.resources.get(Resource.SWORD_INTENT) == 2
