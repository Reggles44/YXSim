from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect, Resource


class CardType(Card):
    display_name = 'Spritiage Sword'
    phase = 2
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        gain_qi = 2
        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.QI: gain_qi
            },
            related_actions=[
                Action(card=self, source=attacker, target=defender, damage=2) for _ in range(2)
            ] if self.source.resources.get(Resource.QI) >= 3 - gain_qi else None
        ).execute()