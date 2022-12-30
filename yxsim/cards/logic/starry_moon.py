from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing


class CardType(Card):
    display_name = 'Starry Moon'
    phase = 3
    sect = Sect.HEPTASTAR
    qi = 0

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.STAR_POWER: 2}),
                Action(card=self, source=attacker, target=attacker, star_points=attacker.next_slot(2))
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = []
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.STAR_POWER] == 2
        assert card_user.star_slots == [1,2]
        assert card_user.resources[Resource.QI] == 0

    def test_card_qi(self):
        card_user, opponent = self.generate_test_data()
        card_user.star_slots = [1,2]
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.STAR_POWER] == 2
        assert card_user.star_slots == [1,2]
        assert card_user.resources[Resource.QI] == 2

    def test_card_wrap(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id for _ in range(7)]})
        card_user.card_counter = 5
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.STAR_POWER] == 2
        assert set(card_user.star_slots) == {0,6}
        assert card_user.resources[Resource.QI] == 0


