from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue, ReferenceValue


class CardType(Card):
    display_name = 'Revitalized'
    phase = 3
    qi = 1

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=attacker.resources[Resource.TOTAL_HEALING]//5 + 10
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 10

    def test_card_much_healing(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI]  = 1
        card_user.resources[Resource.TOTAL_HEALING] = 17
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-13

    def test_card_active_healing(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'health': 50, 'max_health': 100, 'cards': ['great_recovery_elixir', self.id]})
        card_user.resources[Resource.QI]  = 1
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health-12

