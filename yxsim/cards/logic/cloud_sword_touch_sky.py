from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Cloud Sword Touch Sky'
    cloud_hit = True
    phase = 1
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=6,
        ).execute()