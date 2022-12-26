from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Thunder Sword'

    def play(self, attacker, defender, **kwargs) -> bool:
        starting_defender_health = defender.health

        base_attack = Action(source=attacker, target=defender, damage=5)
        success = base_attack.execute()

        if defender.health < starting_defender_health:
            Action(source=attacker, target=defender, damage=6).execute()

        return success