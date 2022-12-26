from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    id = 'Sword Defense'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(source=attacker, target=defender, resource_changes={Resource.SWORD_INTENT: 2, Resource.DEF: 4}).execute()
