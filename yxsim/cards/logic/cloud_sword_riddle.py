from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Cloud Sword Riddle'
    phase = 2
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            cloud_hit_action=Action(card=self, source=attacker, target=defender, damage=9)
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data(player_kwargs={'cards': [self.id]*2})
        combat(p1, p2, limit=3)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user: Player, opponent: Player):
        assert opponent.max_health == opponent.health + 9
