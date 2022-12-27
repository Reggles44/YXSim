from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Cloud Sword Fleche'

    def play(self, attacker, defender, **kwargs) -> bool:
        damage = 5
        # TODO If Cloud Hit do 3 more damage

        return Action(card_id=self.id, source=attacker, target=defender, damage=5).execute()