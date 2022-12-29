from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Inspiration Sword'
    phase = 4
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card=self,
                source=attacker,
                target=attacker,
                resource_changes=ReferenceValue(lambda source: {Resource.SWORD_INTENT: min(8, source.resources[Resource.QI])})
            )
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        card_user.resources[Resource.QI] = 50
        combat(card_user, opponent, limit=1)
        assert card_user.resources[Resource.SWORD_INTENT] == 8
        assert opponent.health == opponent.max_health - 8
