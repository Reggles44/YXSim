from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Mirror Flower Sword Formation'
    phase = 3
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: 3}),
                Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda source: source.resources.get(Resource.DEF)))
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.DEF] == 3
        assert opponent.health == opponent.max_health - 3

    def test_card_much_def(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.DEF] = 20
        combat(card_user, opponent, limit=1)
        # Defense halves at start of turn
        assert card_user.resources[Resource.DEF] == 13
        assert opponent.health == opponent.max_health - 13