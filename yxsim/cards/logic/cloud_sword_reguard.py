from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat


class CardType(Card):
    display_name = 'Cloud Sword Reguard'
    phase = 2
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 8
            },
            cloud_hit_action=Action(card=self, source=attacker, target=attacker, healing=3)
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data(player_kwargs={'cards': ['normal_attack', 'normal_attack', self.id, self.id]})
        combat(p1, p2, limit=7)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user, opponent):
        assert card_user.health == card_user.max_health - 3
        assert card_user.resources.get(Resource.DEF) == 10
        assert card_user.resources.get(Resource.CLOUD_HIT) == 2
