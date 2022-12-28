from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Form-Intention Sword'
    phase = 2
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card=self,
                source=attacker,
                target=defender,
                resource_changes={Resource.SWORD_INTENT: 3},
            )
        ).execute()