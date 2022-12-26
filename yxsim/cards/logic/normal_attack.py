from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Normal Attack'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(source=attacker, target=defender, damage=3).execute()