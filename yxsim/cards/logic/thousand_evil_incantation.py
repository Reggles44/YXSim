from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue


class CardType(Card):
    display_name = 'Thousand Evil Incantation' \
                   ''
    phase = 1

    job = Job.FULULIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            resource_changes={
                Resource.INTERNAL_INJURY: 2,
                Resource.FLAW: 2,
                Resource.WEAKENED: 1
            }
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.resources[Resource.INTERNAL_INJURY] == 2
        assert opponent.resources[Resource.FLAW] == 2
        assert opponent.resources[Resource.WEAKENED] == 1

