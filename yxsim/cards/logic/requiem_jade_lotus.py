from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Requiem Jade Lotus'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            healing=15,
            max_hp_change=15,
            resource_changes={Resource.REGENERATION: 1}, # TODO make regen work
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'max_health': 2})
        card_user.health = 1
        combat(card_user, opponent, limit=1)
        assert card_user.health == 16
        assert card_user.max_health == 17
        assert opponent.resources[Resource.REGENERATION] == 1
