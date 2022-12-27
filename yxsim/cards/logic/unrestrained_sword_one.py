from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Unrestrained Sword - One'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=5 + attacker.unrestrained_sword_counter*2,
        ).execute()