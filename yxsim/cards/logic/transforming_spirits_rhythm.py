from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Transforming Spirits Rhythm'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: 'Player', defender: 'Player', **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.QI: 3
            }
        ).execute()