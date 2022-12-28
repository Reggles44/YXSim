from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Giant Tiger Spirit Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(card=self, source=attacker, target=defender, damage=10).execute()