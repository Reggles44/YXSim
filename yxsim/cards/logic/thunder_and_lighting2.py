from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import RandomValue
from yxsim.events import OnResourceLoss


class ThunderAndLightingOnResourceLoss(OnResourceLoss):
    def handle(self, target: Player, resource: Resource, change: int, **kwargs):
        if resource == Resource.HEXAGRAM and change < 0:
            Action(card=self.source_card, source=target, target=target, resource_changes={Resource.QI: 1}).execute()

class CardType(Card):
    display_name = 'Thunder and Lighting 2'
    phase = 4

    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        listener = ThunderAndLightingOnResourceLoss(source=attacker, source_card=self, priority=0)
        attacker.add_listener(listener)
        result = Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=RandomValue(1, 10)) for _ in range(2)
            ]
        ).execute()
        attacker.remove_listener(listener)
        return result


    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'health': 50, 'max_health': 100})
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-10
        assert card_user.resources[Resource.QI] == 0

    def test_card_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'health': 50, 'max_health': 100})
        card_user.resources[Resource.HEXAGRAM] = 2
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-20
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.QI] == 2

    def test_card_one_hexagram(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'health': 50, 'max_health': 100})
        card_user.resources[Resource.HEXAGRAM] = 1
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health-15
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.QI] == 1

    def test_card_one_hexagram_test(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'random_setting': 'mean', 'cards': [self.id, 'palm_thunder']})
        card_user.resources[Resource.HEXAGRAM] = 3
        combat(card_user, opponent, limit=3)
        assert card_user.resources[Resource.HEXAGRAM] == 0
        assert card_user.resources[Resource.QI] == 2