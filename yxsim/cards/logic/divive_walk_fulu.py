from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Divive Walk Fulu'
    phase = 1

    job = Job.FULULIST
    consumtion = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        return Action(
            card=self,
            source=attacker,
            target=defender,
            chase=True,
            resource_changes={Resource.QI: 2}
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6
        assert card_user.resources[Resource.QI] == 1
