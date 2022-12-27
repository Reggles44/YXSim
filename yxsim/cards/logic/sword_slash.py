from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    display_name = 'Sword Slash'

    def play(self, attacker, defender, **kwargs) -> bool:
        sword_intent_buff = Action(card_id=self.id, source=attacker, target=defender, resource_changes={Resource.SWORD_INTENT: 2})
        return Action(card_id=self.id, source=attacker, target=defender, damage=3, related_actions=[sword_intent_buff]).execute()