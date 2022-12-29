import typing

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Flying Spirit Shade Sword'
    phase = 4
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
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

    def test_card(self):
        card_user, opponent = super().generate_test_data()
        opponent.resources[Resource.DEF] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 3
        assert card_user.resources.get(Resource.QI) == 3
