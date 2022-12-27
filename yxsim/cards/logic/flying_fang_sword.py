from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.resources import Resource


class CardType(Card):
    display_name = 'Sword Defense'

    def play(self, attacker, defender, **kwargs) -> bool:
        return Action(
            card_id=self.id, source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card_id=self.id,
                source=attacker,
                target=attacker,
                resource_changes={
                    Resource.SWORD_INTENT: attacker.resources[Resource.SWORD_INTENT]
                }
            )
        ).execute()
