from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd, OnTurnStart
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Anthomania Formation'
    phase = 1

    job = Job.FORMATION

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        # TODO does this card increase qi gain or multiple qi gain
        # TODO would multicasting this card make it 4x, 8x, 16x or +4, +6, +8
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.QI_GAIN_MULTIPLIER: 1}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'guard_qi']})
        combat(card_user, opponent, limit=3)
        assert card_user.resources[Resource.QI_GAIN_MULTIPLIER] == 2 # If this value is not 2 then the default of 1 was not set
        assert card_user.resources[Resource.QI] == 2
