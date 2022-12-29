from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.player import Player
from yxsim.resources import Sect, Resource
from yxsim.combat import combat
from yxsim.events import OnTurnStart
from yxsim.util import ReferenceValue


class ReflexiveSwordOnTurnStart(OnTurnStart):
    def handle(self, attacker: Player, defender: Player, **kwargs):
        if self.enabled:
            Action(card=self.source_card, event=True, source=attacker, target=attacker, resource_changes={Resource.DEF: 6}).execute()
        self.enabled = False


class CardType(Card):
    display_name = 'Reflexive Sword'
    phase = 3
    sect = Sect.CLOUD
    qi = 1

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        return Action(
            card=self,
            source=attacker,
            target=defender,
            damage=10,
            injured_action=Action(
                card=self,
                source=attacker,
                target=attacker,
                damage=ReferenceValue(lambda source: attacker.add_listener(ReflexiveSwordOnTurnStart(source=attacker, source_card=self, priority=0))))
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=3)
        assert opponent.health == opponent.max_health - 13
        assert card_user.resources[Resource.DEF] == 6

    def test_card_two_electric_boogaloo(self):
        card_user, opponent = self.generate_test_data()
        card_user.resources[Resource.QI] = 1
        combat(card_user, opponent, limit=5)
        assert opponent.health == opponent.max_health - 16
        assert card_user.resources[Resource.DEF] == 1