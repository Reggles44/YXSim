from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Cloud Sword Touch Sky'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(card_id=self.id, source=attacker, target=defender, damage=6).execute()