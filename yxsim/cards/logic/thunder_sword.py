from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Thunder Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            qi=1,
            card_id=self.id, source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card_id=self.id, source=attacker, target=defender, damage=6)
        ).execute()