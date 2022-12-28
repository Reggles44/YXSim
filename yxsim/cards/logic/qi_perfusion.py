from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Qi Perfusion'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.QI: 2,
                Resource.IGNORE_DEFENSE: 1
            }
        ).execute()