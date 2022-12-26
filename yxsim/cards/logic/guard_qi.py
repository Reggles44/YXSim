from yxsim.resources import Resource
from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Guard Qi'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 5, Resource.QI: 1
            }
        ).execute()