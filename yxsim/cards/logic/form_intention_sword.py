from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Form-Intention Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            qi=1,
            card_id=self.id, source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(card_id=self.id, source=attacker, target=defender, resource_changes={Resource.SWORD_INTENT:3}, unrestrained_sword=True)
        ).execute()