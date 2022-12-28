import typing

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Normal Attack'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=defender,
                    damage=1,
                    injured_action=Action(
                        card=self,
                        source=attacker,
                        target=attacker,
                        resource_changes={Resource.QI: 1}
                    )
                ) for _ in range(4)
            ]
        ).execute()

    def generate_test_data(self) -> typing.Tuple[Player, Player]:
        player, enemy = super().generate_test_data()
        enemy.resources[Resource.DEF] = 1
        return player, enemy

    def asserts(self, card_user: 'Player', opponent: 'Player'):
        assert opponent.health == opponent.max_health - 3
        assert card_user.resources.get(Resource.QI) == 3