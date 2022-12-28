from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Unrestrained Sword - One'
    phase = 2
    sect = Sect.CLOUD
    unrestrained_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5 + attacker.resources[Resource.UNRESTRAINED_SWORD_COUNTER]*2,
        ).execute()