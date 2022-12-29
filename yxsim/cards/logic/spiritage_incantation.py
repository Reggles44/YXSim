from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue, ReferenceValue


class CardType(Card):
    display_name = 'Spirtage Incantation Fulu'
    phase = 1

    job = Job.FULULIST

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            # TODO this is wrong if there is something that changes the amount of QI gained
            resource_changes=ReferenceValue(
                lambda source: {Resource.DEF: source.resources[Resource.QI]+3, Resource.QI: 3}
            )
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 4
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 7
        assert card_user.resources[Resource.DEF] == 7

