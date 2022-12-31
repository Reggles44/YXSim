from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.events import OnDefend


class RepelCittaDharmaOnGainResource(OnDefend):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        Action(card=self.source_card, source=defender, target=attacker, event=True, damage=2, attack=False).execute()


class CardType(Card):
    display_name = 'Repel Citta Dharma'
    phase = 4
    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(RepelCittaDharmaOnGainResource(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(card_user, opponent, limit=2)

        assert opponent.health == opponent.max_health - 2





