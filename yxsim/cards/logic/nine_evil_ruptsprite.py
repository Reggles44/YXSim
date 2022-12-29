from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Nine Evil Ruptsprite'
    phase = 2

    job = Job.ELIXIRIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=target,
                    resource_changes={Resource.QI: -3}
                ) for target in [attacker, defender]
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()

        card_user.resources[Resource.QI] = 4
        opponent.resources[Resource.QI] = 4

        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 1
        assert opponent.resources[Resource.QI] == 1
