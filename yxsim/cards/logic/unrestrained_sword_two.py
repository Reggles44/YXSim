from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
import typing
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Unrestrained Sword - Two'
    phase = 4
    sect = Sect.CLOUD
    unrestrained_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=ReferenceValue(lambda source: [Action(card=self, source=attacker, target=defender, damage=4) for _ in range(source.resources[Resource.UNRESTRAINED_SWORD_COUNTER]+1)]),
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': ['normal_attack', self.id, self.id]})
        combat(card_user, opponent, limit=5)
        assert opponent.health == opponent.max_health - 15  # 3 + 4 + 4*2
