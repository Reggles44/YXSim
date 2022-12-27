from yxsim.resources import Resource
from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Light Sword'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=4,
            related_actions=[
                Action(
                    card_id=self.id,
                    source=attacker,
                    target=attacker,
                    resource_changes={
                        Resource.QI: 1
                    }
                )
            ]
        ).execute()