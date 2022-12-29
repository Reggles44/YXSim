from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Cloud Sword Flash Wind'
    phase = 4
    sect = Sect.CLOUD
    cloud_sword = True
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=4,
            cloud_hit_action=Action(card=self, source=attacker, target=attacker, chase=True)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 4

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id for _ in range(2)]})
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health - 11
