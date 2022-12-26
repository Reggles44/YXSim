from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Thunder Sword'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(source=attacker, target=defender, damage=6)
        ).execute()