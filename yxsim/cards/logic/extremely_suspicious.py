from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import ReferenceValue

class CardType(Card):
    display_name = 'Extremely Suspicious'
    phase = 4

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(
                    card=self, source=attacker, target=defender, resource_changes={Resource.INTERNAL_INJURY: 2}
                ),
                Action(
                    card=self, event=True, source=attacker, target=defender, damage=ReferenceValue(lambda target: target.resources[Resource.INTERNAL_INJURY] or None), ignore_armor=True
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.resources[Resource.INTERNAL_INJURY] == 2
        assert opponent.health == opponent.max_health - 2
