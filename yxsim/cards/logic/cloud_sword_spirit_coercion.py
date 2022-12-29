from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue

class CardType(Card):
    display_name = 'Cloud Sword Spirit Coercion'
    phase = 3
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=7,
            cloud_hit_action=Action(card=self, source=attacker, target=attacker, resource_changes=ReferenceValue(lambda source: {Resource.QI: source.resources[Resource.CLOUD_HIT_COUNTER]}))
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id for _ in range(3)]})
        combat(card_user, opponent, limit=5)
        assert opponent.max_health == opponent.health + 21
        assert card_user.resources[Resource.QI] == 3
        assert card_user.resources[Resource.CLOUD_HIT_COUNTER] == 3

    def test_card_large_counter(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        card_user.resources[Resource.CLOUD_HIT_COUNTER] = 8
        combat(card_user, opponent, limit=1)
        assert opponent.max_health == opponent.health + 7
        assert card_user.resources[Resource.QI] == 8
