from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Sword Defense'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.SWORD_INTENT: 2,
                Resource.DEF: 4
            }).execute()

    def asserts(self, card_user: Player, opponent: Player):
        assert card_user.resources.get(Resource.SWORD_INTENT) == 2
        assert card_user.resources.get(Resource.DEF) == 4
