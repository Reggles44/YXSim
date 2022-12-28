from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource

class CardType(Card):
    display_name = 'Cloud Sword Touch Sky'
    cloud_hit = True
    phase = 1
    sect = Sect.CLOUD
    cloud_sword = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=6,
        ).execute()

    def asserts(self, card_user, opponent):
        assert opponent.max_health == opponent.health + 6
        assert card_user.resources.get(Resource.CLOUD_HIT) == 1