from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.events import OnResourceGain


class StillnessCittaDharmaOnGainResource(OnResourceGain):
    def handle(self, target: Player, resource: Resource, change: int, **kwargs):
        if resource == Resource.QI:
            Action(card=self.source_card, source=target, target=target, healing=2*change).execute()


class CardType(Card):
    display_name = 'Stillness Citta Dharma'
    phase = 2
    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(StillnessCittaDharmaOnGainResource(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'normal_attack', 'qi_perfusion']})
        combat(card_user, opponent, limit=5)

        assert card_user.health == card_user.max_health - 2





