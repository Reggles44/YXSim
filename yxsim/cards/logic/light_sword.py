from yxsim.resources import Resource
from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Light Sword'

    def play(self, attacker, defender, **kwargs) -> bool:
        qi_buff = Action(source=attacker, target=attacker, resource_changes={Resource.QI: 1})
        return Action(source=attacker, target=defender, damage=4, related_actions=[qi_buff]).execute()