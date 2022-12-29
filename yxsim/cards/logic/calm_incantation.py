from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Calm Incantation'
    phase = 1

    job = Job.FULULIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                debuff: -2 for debuff in Resource.debuffs()
            }
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()

        for debuff in Resource.debuffs():
            card_user.resources[debuff] += 2

        combat(card_user, opponent, limit=1)

        for debuff in Resource.debuffs():
            assert card_user.resources[debuff] == 0
