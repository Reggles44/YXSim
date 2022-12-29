import random

from yxsim.action import Action
from yxsim.cards.base import Card
from yxsim.combat import combat
from yxsim.player import Player
from yxsim.resources import Sect, Job, Resource
from yxsim.util import ReferenceValue


class CardType(Card):
    display_name = 'Exorcism Elixir'
    phase = 1

    job = Job.ELIXIRIST
    consumption = True

    def play(self, attacker: Player, defender: Player, **kwargs) -> bool:
        self.exhausted = True

        def random_debuff(source):
            available_debuffs = list(filter(bool, set(source.resources.keys()) & set(Resource.debuffs())))
            if available_debuffs:
                return {random.choice(available_debuffs): -3}

        return Action(
            card=self,
            source=attacker,
            target=attacker,
            resource_changes={Resource.DEF: 8},
            related_actions=[
                Action(
                    card=self,
                    source=attacker,
                    target=attacker,
                    resource_changes=ReferenceValue(random_debuff)
                ) for _ in range(2)
            ]
        ).execute()

    def test_card(self):
        card_user, opponent = self.generate_test_data()

        card_user.resources[Resource.WEAKENED] = 3
        card_user.resources[Resource.FLAW] = 3

        combat(card_user, opponent, limit=1)

        assert card_user.resources[Resource.WEAKENED] == 0
        assert card_user.resources[Resource.FLAW] == 0

    def test_remove_same_buff_twice(self):
        card_user, opponent = self.generate_test_data()

        card_user[random.choice(Resource.debuffs())] = 6

        combat(card_user, opponent, limit=1)
        assert all(card_user.resources[debuff] == 0 for debuff in Resource.debuffs())
