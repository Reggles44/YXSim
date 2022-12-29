from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Resource, Sect


class CardType(Card):
    display_name = 'CentiBird Spirit Sword Formation'
    phase = 3
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.SPIRIT_SWORD_DISCOUNT: 1, Resource.QI: 1
            }
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'giant_tiger_spirit_sword', 'thunder_sword']})
        card_user.resources[Resource.QI] = 10
        combat(card_user, opponent, limit=5)
        assert card_user.resources[Resource.QI] == 10  # 10 + 1 - 0 - 1
        assert opponent.health == opponent.max_health - 21
