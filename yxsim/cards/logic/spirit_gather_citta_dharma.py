from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.events import OnTurnStart


class SpiritGatherCittaDharmaOnTurnStart(OnTurnStart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mod = 1

    def handle(self, attacker: Player, defender: Player, **kwargs):
        if self.mod%2 == 0:
            Action(card=self.source_card, source=attacker, target=attacker, resource_changes={Resource.QI: 1}).execute()
        self.mod += 1


class CardType(Card):
    display_name = 'Spirit Gather Citta Dharma'
    phase = 4
    sect = Sect.CLOUD

    def play(self, attacker: Player, defender: Player, **kwargs) -> Action:
        self.exhausted = True
        attacker.add_listener(SpiritGatherCittaDharmaOnTurnStart(source=attacker, source_card=self, priority=0))
        return Action(card=self, source=attacker, target=attacker).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(card_user, opponent, limit=3)
        assert card_user.resources[Resource.QI] == 0

        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(card_user, opponent, limit=5)
        assert card_user.resources[Resource.QI] == 1

        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(card_user, opponent, limit=7)
        assert card_user.resources[Resource.QI] == 1

        card_user, opponent = self.generate_test_data(player_kwargs={'cards': [self.id]})
        combat(card_user, opponent, limit=9)
        assert card_user.resources[Resource.QI] == 2
