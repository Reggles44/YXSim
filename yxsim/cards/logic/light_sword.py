from yxsim.resources import Sect, Resource
from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player

class CardType(Card):
    display_name = 'Light Sword'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=4,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes={
                        Resource.QI: 1
                    }
                )
            ]
        ).execute()