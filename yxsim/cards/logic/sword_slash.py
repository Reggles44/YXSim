from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    id = 'Sword Slash'

    def play(self, attacker, defender, **kwargs) -> bool:
        sword_intent_buff = Action(source=attacker, target=defender, resource_changes={Resource.SWORD_INTENT: 2})
        return Action(source=attacker, target=defender, damage=3, related_actions=[sword_intent_buff]).execute()