from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    id = 'Cloud Sword Fleche'

    def play(self, attacker, defender, **kwargs) -> bool:
        damage = 5
        # TODO If Cloud Hit do 3 more damage

        return Action(source=attacker, target=defender, damage=5).execute()