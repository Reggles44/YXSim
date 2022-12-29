from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource


class CardType(Card):
    display_name = 'Carefree Tune'
    phase = 1

    job = Job.MUSICIAN
    continuous = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True
        for card in attacker.cards + defender.cards:
            if card.id == 'normal_attack':
                card.damage += 4

        return Action(card=self, source=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        combat(card_user, opponent, limit=3)
        assert card_user.health == card_user.max_health - 7
        assert opponent.health == opponent.max_health - 7