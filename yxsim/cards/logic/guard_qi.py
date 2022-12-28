from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Resource, Sect


class CardType(Card):
    display_name = 'Guard Qi'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 5, Resource.QI: 1
            }
        ).execute()

    def asserts(self, card_user: Player, opponent: Player):
        assert card_user.resources.get(Resource.DEF) == 5
        assert card_user.resources.get(Resource.QI) == 1
