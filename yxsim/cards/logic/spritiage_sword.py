from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Spritiage Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        gain_qi = 2
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.QI: gain_qi}),
                *[Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda source: 2 if source.resources[Resource.QI] > 2 else None)) for _ in range(2)]
            ]
        ).execute()

    def asserts(self, card_user: Player, opponent: Player):
        assert card_user.resources.get(Resource.QI) == 2
        assert opponent.max_health == opponent.health

    def test_much_qi(self):
        p1, p2 = self.generate_test_data()
        p1.resources[Resource.QI] = 1
        combat(p1, p2, limit=1)
        assert p1.resources.get(Resource.QI) == 3
        assert p2.max_health == p2.health + 4
        return p1, p2

    def generate_test_data(self, player_kwargs=None, enemy_kwargs=None) -> typing.Tuple[Player, Player]:
        player_kwargs = player_kwargs or {'cards': [self.id]}
        enemy_kwargs = enemy_kwargs or {'cards': []}
        return Player(id="PLAYER", **player_kwargs), Player(id='ENEMY', **enemy_kwargs)


    #  TODO test - double qi works when it previously wouldn't trigger