from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Cloud Sword Fleche'
    phase = 1
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:
        damage = 5

        cloud_hit_action = Action(card=self, source=attacker, target=defender, damage=3)
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=5,
            cloud_hit_action=cloud_hit_action
        ).execute()