from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    id = 'Sword Defense'

    def play(self, attacker, defender, **kwargs) -> bool:
        starting_defender_health = defender.health
        starting_sword_intent = attacker.resource[Resource.SWORD_INTENT]

        base_attack = Action(source=attacker, target=defender, damage=5)
        success = base_attack.execute()

        if defender.health < starting_defender_health:
            Action(source=attacker, target=attacker, resource_changes={Resource.SWORD_INTENT: starting_sword_intent}).execute()

        return success