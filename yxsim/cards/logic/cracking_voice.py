from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Cracking Voice'
    phase = 1

    job = Job.MUSICIAN

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=6,
            ignore_armor=True
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        opponent.resources[Resource.DEF] = 100
        combat(card_user, opponent, limit=1)
        assert opponent.health == opponent.max_health - 6