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

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            cloud_hit_action=Action(card=self, source=attacker, target=defender, damage=9)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]*2})
        combat(card_user, opponent, limit=3)
        assert opponent.max_health == opponent.health + 9
