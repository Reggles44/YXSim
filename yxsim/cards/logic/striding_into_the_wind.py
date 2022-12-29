from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue, ReferenceValue


class CardType(Card):
    display_name = 'Striding Into The Wind'
    phase = 1

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                *[Action(card=self, source=attacker, target=defender, damage=3) for _ in range(2)],
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: RandomValue(2,10).cast(source=attacker)})
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-6
        assert card_user.resources[Resource.DEF] == 6

    def test_card_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean'})
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-6
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.DEF] == 10


