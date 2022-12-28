from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Sword Slash'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=3,
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes={Resource.SWORD_INTENT: 2}
                )
            ]
        ).execute()