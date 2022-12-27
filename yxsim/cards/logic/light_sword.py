from yxsim.resources import Sect, Resource
from yxsim.action import Action
from yxsim.cards.base import Card


class CardType(Card):
    display_name = 'Light Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=4,
            related_actions=[
                Action(
                    resource_changes={
                        Resource.QI: 1
                    }
                )
            ]
        ).execute()