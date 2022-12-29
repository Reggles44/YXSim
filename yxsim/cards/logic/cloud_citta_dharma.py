from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect
from yxsim.events import OnPlayCard


class CloudCittaDharmaOnPlayCard(OnPlayCard):
    def handle(self, card: Card, attacker: Player, defender: Player, **kwargs):
        if card.cloud_sword is True:
            Action(card=self.source_card, source=attacker, target=attacker, healing=2).execute()


class CardType(Card):
    display_name = 'Cloud Citta Dharma'
    phase = 1
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(CloudCittaDharmaOnPlayCard(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'cloud_sword_fleche']})
        combat(card_user, opponent, limit=3)

        # TODO Make a real test here
        assert card_user.health == card_user.max_health - 1



