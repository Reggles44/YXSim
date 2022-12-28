from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Sword Defense'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            resource_changes={
                Resource.SWORD_INTENT: 2,
                Resource.DEF: 4
            }).execute()
