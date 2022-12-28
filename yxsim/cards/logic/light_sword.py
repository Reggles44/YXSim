from yxsim.combat import combat
from yxsim.resources import Sect, Resource
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player

class CardType(Card):
    display_name = 'Light Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=4,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes={
                        Resource.QI: 1
                    }
                )
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 4
        assert card_user.resources.get(Resource.QI) == 1
