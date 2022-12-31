from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.events import OnResourceGain


class HexagramFormacideOnGainResource(OnResourceGain):
    def handle(self, target: Player, resource: Resource, change: int, **kwargs):
        if resource == Resource.HEXAGRAM and change > 0:
            Action(card=self.source_card, source=target, target=target.opponent, damage=3*change).execute()


class CardType(Card):
    display_name = 'Hexagram Formacide'
    phase = 4
    sect = Sect.HEPTASTAR

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(HexagramFormacideOnGainResource(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=defender).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'lake_hexagram']})
        combat(card_user, opponent, limit=3)

        assert opponent.health == opponent.max_health - 6


    def test_card_guardup(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id, 'lake_hexagram']})
        opponent.resources[Resource.GUARD_UP] = 1
        combat(card_user, opponent, limit=3)

        assert opponent.health == opponent.max_health


