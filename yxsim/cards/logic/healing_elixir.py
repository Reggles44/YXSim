from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Healing Elixir'
    phase = 1

    job = Job.ELIXIRIST
    consumption = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            healing=ReferenceValue(lambda source: source.resources[Resource.QI] + 7)
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.health -= 20
        card_user.resources[Resource.QI] = 4
        combat(card_user, opponent, limit=1)
        assert card_user.health == card_user.max_health - 9
