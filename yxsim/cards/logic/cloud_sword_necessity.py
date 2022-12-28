from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.player import Player
import typing


class CardType(Card):
    display_name = 'Cloud Sword Necessity'
    phase = 1
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        cloud_hit_action = Action(card=self, source=attacker, target=attacker, resource_changes={Resource.IGNORE_DEF: 1})
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=4) for _ in range(2)
            ],
            cloud_hit_action=cloud_hit_action
        ).execute()

    def test_cards(self):
        return [self.id, self.id]

    def test_limit(self):
        return 3

    def asserts(self, card_user: 'Player', opponent: 'Player'):
        assert opponent.max_health == opponent.health + 16
        assert card_user.resources.get(Resource.IGNORE_DEF) == 1