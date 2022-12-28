from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Wind Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(card=self, source=attacker, target=defender, related_actions=[
            Action(card=self, source=attacker, target=defender, damage=3) for _ in range(2)
        ]).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data()
        p1.resources[Resource.SWORD_INTENT] = 5
        combat(p1, p2, limit=1)
        assert p2.max_health == p2.health + 16
        return p1, p2

    def test_sword_intent(self):
        p1, p2 = self.generate_test_data_multi()
        p1.resources[Resource.SWORD_INTENT] = 5
        combat(p1, p2, limit=3)
        assert p2.max_health == p2.health + 16+6
        return p1, p2

    def generate_test_data_multi(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        player_kwargs = player_kwargs or {'cards': [self.id, self.id]}
        enemy_kwargs = enemy_kwargs or {'cards': []}
        p1 = Player(id="PLAYER", **player_kwargs)
        p2 = Player(id='ENEMY', **enemy_kwargs)
        return p1, p2
