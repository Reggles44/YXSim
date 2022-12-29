from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Cloud Sword Step Lightly'
    phase = 5
    sect = Sect.CLOUD
    cloud_sword = True
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=2, chase=True) for _ in range(2)
            ],
            cloud_hit_action=Action(card=self, source=attacker, target=attacker, resource_changes=ReferenceValue(lambda source: {Resource.DEF: source.resources[Resource.CLOUD_HIT_COUNTER]*3})),
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': ['cloud_sword_touch_sky', 'normal_attack', 'cloud_sword_touch_sky', 'cloud_sword_touch_sky', self.id]})
        card_user.resources[Resource.CLOUD_HIT_COUNTER] = 1
        combat(card_user, opponent, limit=9)

        assert card_user.resources[Resource.DEF] == 6
