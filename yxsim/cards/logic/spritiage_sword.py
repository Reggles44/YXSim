from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.util import ReferenceValue

class CardType(Card):
    display_name = 'Spritiage Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        gain_qi = 2
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.QI: gain_qi
            },
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=ReferenceValue(lambda source: 2 if source.resources[Resource.QI] > 2 else None)) for _ in range(2)
            ]
        ).execute()

    # TODO when we have the ability to do multiple testst test
    # - works normally
    # - doesn't trigger
    # - double qi works when it previously wouldn't trigger