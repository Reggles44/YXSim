from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Giant Whale Spirit Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            qi=2,
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=16
        ).execute()