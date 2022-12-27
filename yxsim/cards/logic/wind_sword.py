from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Wind Sword'

    def play(self, attacker, defender, **kwargs) -> bool:

        return Action(card_id=self.id, source=attacker, target=defender, related_actions=[
            Action(card_id=self.id, source=attacker, target=defender, damage=3) for _ in range(2)
        ]).execute()