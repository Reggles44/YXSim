from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Earth Evil Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(card=self, source=attacker, target=attacker, resource_changes=ReferenceValue(lambda parent: {Resource.DEF: parent.damage_to_health}))
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(p1, p2, limit=3)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user, opponent):
        assert card_user.resources.get(Resource.DEF) == 8
        assert opponent.health == opponent.max_health - 8
