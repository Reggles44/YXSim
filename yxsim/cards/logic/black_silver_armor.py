from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Black Silver Armor'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: 7}),
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes=ReferenceValue(lambda source: {Resource.DEF: source.resources[Resource.DEF]})
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.DEF] = 10  # halves to 5
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.DEF] == 24
