from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Thunder Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5,
            injured_action=Action(card=self, source=attacker, target=defender, damage=6)
        ).execute()