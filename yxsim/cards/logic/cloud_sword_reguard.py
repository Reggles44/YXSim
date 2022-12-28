from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Cloud Sword Reguard'
    phase = 2
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker, defender, **kwargs) -> bool:

        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 8
            },
            cloud_hit_action=Action(card=self, source=attacker, target=attacker, healing=3)
        ).execute()

