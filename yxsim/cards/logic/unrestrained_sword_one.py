from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Unrestrained Sword - One'
    phase = 2
    sect = Sect.CLOUD
    unrestrained_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5 + attacker.resources.get(Resource.UNRESTRAINED_SWORD_COUNTER)*2,
        ).execute()