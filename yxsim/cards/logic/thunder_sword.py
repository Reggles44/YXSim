from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Thunder Sword'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id, source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card_id=self.id, source=attacker, target=defender, damage=6)
        ).execute()