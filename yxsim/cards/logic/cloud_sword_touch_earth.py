from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Cloud Sword Touch Earth'
    cloud_hit = True
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=6,
            cloud_sword=True
        ).execute()