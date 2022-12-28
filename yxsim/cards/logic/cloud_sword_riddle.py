from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Cloud Sword Riddle'
    phase = 2
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            cloud_hit_action=Action(card=self, source=attacker, target=defender, damage=9)
        ).execute()

    def test_cards(self):
        return [self.id, self.id]

    def test_limit(self):
        return 3

    def asserts(self, card_user, opponent):
        assert opponent.max_health == opponent.health + 9
