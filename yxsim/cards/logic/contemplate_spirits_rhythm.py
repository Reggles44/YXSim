from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Consonance Sword Formation'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        si = attacker.resources.get(Resource.SWORD_INTENT),
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_exhaust={
                Resource.SWORD_INTENT:si,
            },
            resource_changes={
                Resource.QI: si,
                Resource.DEF: 9
            }
        ).execute()