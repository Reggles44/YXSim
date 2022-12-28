from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Giant Whale Spirit Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 2

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=16
        ).execute()