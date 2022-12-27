from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Sect


class CardType(Card):
    display_name = 'Cloud Sword Fleche'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker, defender, **kwargs) -> bool:
        damage = 5

        cloud_hit_action = Action(card_id=self.id, source=attacker, target=defender, damage=3)
        return Action(
            card_id=self.id,
            source=attacker,
            target=defender,
            damage=5,
            cloud_sword=True,
            cloud_hit_action=cloud_hit_action
        ).execute()