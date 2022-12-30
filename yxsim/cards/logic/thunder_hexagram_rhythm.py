from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue, ReferenceValue


class CardType(Card):
    display_name = 'Thunder Hexagram Rhythm'
    phase = 3

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=RandomValue(1,9)),
                Action(card=self, source=attacker, target=attacker, resource_changes=ReferenceValue(lambda source: {Resource.HEXAGRAM: min(source.resources[Resource.SPENT_HEXAGRAM], 3)}))
        ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-5
        assert card_user.resources[Resource.HEXAGRAM] == 0

    def test_card_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-9
        assert card_user.resources[Resource.HEXAGRAM] == 1

    def test_card_hexagram_much(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'cards': [self.id, self.id]})
        card_user.resources[Resource.HEXAGRAM] = 1
        card_user.resources[Resource.SPENT_HEXAGRAM] = 10
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-9
        assert card_user.resources[Resource.HEXAGRAM] == 3

    def test_card_hexagram_much_twice(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'cards': [self.id, self.id]})
        card_user.resources[Resource.HEXAGRAM] = 1
        card_user.resources[Resource.SPENT_HEXAGRAM] = 10
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health-18
        assert card_user.resources[Resource.HEXAGRAM] == 5

    def test_card_hexagram_small_twice(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'cards': [self.id, self.id]})
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health - 18
        assert card_user.resources[Resource.HEXAGRAM] == 2