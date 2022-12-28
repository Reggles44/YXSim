from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Cloud Sword Touch Earth'
    cloud_hit = True
    phase = 1
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:
        cloud_hit_action = Action(card=self, source=attacker, target=attacker, resource_changes={Resource.DEF: 4})
        return Action(
            card=self,
            source=attacker,
            target=defender,
            cloud_hit_action=cloud_hit_action,
            damage=4,
        ).execute()