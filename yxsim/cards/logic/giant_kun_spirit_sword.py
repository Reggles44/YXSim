from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Giant Kun Spirit Sword'
    phase = 4
    sect = Sect.CLOUD
    qi = 3
    spirit_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            chase=True,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=10),
                Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: 10})
            ],
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id for _ in range(2)]})
        card_user.resources[Resource.QI] = 6
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 0
        assert opponent.health == opponent.max_health - 20
        assert card_user.resources[Resource.DEF] == 20


