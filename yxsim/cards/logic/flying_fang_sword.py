from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Resource, Sect
from yxsim.combat import combat


class CardType(Card):
    display_name = 'Flying Fang Sword'
    phase = 1
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self, source=attacker,
            target=defender,
            damage=8,
            injured_action=Action(
                card=self,
                source=attacker,
                target=attacker,
                resource_changes={
                    Resource.SWORD_INTENT: attacker.resources[Resource.SWORD_INTENT]
                }
            )
        ).execute()

    def test_card(self):
        p1, p2 = self.generate_test_data(player_kwargs={'cards': ['sword_slash', self.id]})
        combat(p1, p2, limit=5)
        self.asserts(p1, p2)
        return p1, p2

    def asserts(self, card_user, opponent):
        assert opponent.health == opponent.max_health - 13
        assert card_user.resources.get(Resource.SWORD_INTENT) == 2
