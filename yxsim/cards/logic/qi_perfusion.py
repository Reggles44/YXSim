from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    id = 'Qi Perfusion'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(source=attacker, target=attacker, resource_changes={Resource.QI: 2, Resource.IGNORE_DEFENSE: 1}).execute()