from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Thunder Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card=self, source=attacker, target=defender, damage=6)
        ).execute()

    def asserts(self, card_user: Player, opponent: Player):
        assert opponent.health == opponent.max_health - 11

    def test_defense_block(self):
        p1, p2 = self.generate_test_data()
        p2.resources[Resource.DEF] = 5
        combat(p1, p2, limit=1)
        assert p2.max_health == p2.health
        return p1, p2

    def test_sword_intent(self):
        p1, p2 = self.generate_test_data()
        p1.resources[Resource.SWORD_INTENT] = 5
        combat(p1, p2, limit=1)
        assert p2.max_health == p2.health + 21
        return p1, p2

    def generate_test_data(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        player_kwargs = player_kwargs or {'cards': [self.id]}
        enemy_kwargs = enemy_kwargs or {'cards': []}
        p1 = Player(id="PLAYER", **player_kwargs)
        p2 = Player(id='ENEMY', **enemy_kwargs)
        p1.resources[Resource.QI] = 1
        return p1, p2
