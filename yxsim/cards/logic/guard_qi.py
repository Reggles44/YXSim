from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource, Sect


class CardType(Card):
    display_name = 'Guard Qi'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, **kwargs) -> bool:
        return Action(
            card_id=self.id,
            source=attacker,
            target=attacker,
            resource_changes={
                Resource.DEF: 5, Resource.QI: 1
            }
        ).execute()