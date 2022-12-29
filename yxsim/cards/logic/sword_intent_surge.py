from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Sword Intent Surge'
    phase = 5
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes=ReferenceValue(lambda source: {Resource.SWORD_INTENT: (source.resources[Resource.SWORD_INTENT]*0.8)//1}),
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, self.id]})
        card_user.resources[Resource.SWORD_INTENT] = 11
        combat(card_user, opponent, limit=3)
        assert card_user.resources[Resource.SWORD_INTENT] == 34
        return card_user, opponent
