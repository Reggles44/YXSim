from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue
from yxsim.combat import combat

class CardType(Card):
    display_name = 'Giant Roc Spirit Sword'
    phase = 3
    sect = Sect.CLOUD
    qi = 2
    spirit_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=9),
                Action(card=self, source=attacker, target=defender, chase=ReferenceValue(lambda source: source.resources.get(Resource.QI) > 0))
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 3
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 1
        assert opponent.health == opponent.max_health - 12

    def test_card_daisy(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id for _ in range(2)]})
        card_user.resources[Resource.QI] = 50
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 46
        assert opponent.health == opponent.max_health - 18

    def test_card_poor(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 2
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.QI] == 0
        assert opponent.health == opponent.max_health - 9