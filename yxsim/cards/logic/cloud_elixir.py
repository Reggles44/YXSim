from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Cloud Elixir'
    phase = 1

    job = Job.ELIXIRIST
    consumption = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(card=self, source=attacker, target=attacker, resource_changes={Resource.IGNORE_DEF: 2, Resource.QI: 2}).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.IGNORE_DEF] == 2
        assert card_user.resources[Resource.QI] == 2
