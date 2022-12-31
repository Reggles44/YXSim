
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.events import OnTurnEnd
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Cosmos Seal Divine Orb'
    phase = 1

    talisman = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=9,
            resource_changes={Resource.WEAKENED: 3}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 9
        assert opponent.resources[Resource.WEAKENED] == 3
