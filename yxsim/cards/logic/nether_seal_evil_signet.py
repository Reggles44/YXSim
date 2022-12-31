from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Nether Seal Evil Signet'
    phase = 1

    talisman = True

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
                    resource_changes={
                        Resource.DEF: -defender.resources[Resource.DEF],
                        Resource.GUARD_UP: -defender.resources[Resource.GUARD_UP]
                    },
                ),
                Action(
                    card=self,
                    source=attacker,
                    target=defender,
                    damage=30
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources.update({Resource.DEF: 999, Resource.GUARD_UP: 999})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 30
