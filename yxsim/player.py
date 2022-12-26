import collections

from yxsim.cards.logic import registry as card_registry
from yxsim.characters.logic import registry as character_registry
from yxsim.destinies.logic import registry as destiny_registry
from yxsim.events import EventManager


class Player(EventManager):
    def __init__(
            self,
            max_health,
            cultivation,
            slots,

            character,
            destinies,
            cards,
            star_slots,

            **kwargs
    ):
        super().__init__()
        self.resources = collections.defaultdict(int)

        self.health = max_health
        self.max_health = max_health
        self.cultivation = cultivation
        self.slots = slots

        self.character = character_registry[character]

        for destiny in destinies:
            self.add_listener(destiny_registry[destiny])

        self.cards = []
        self.cards = [card_registry[cards[i] if i < len(cards) else ''] for i in range(slots)]
        self.star_slots = star_slots
        self.card_counter = 0

    def play_next_card(self, **kwargs):
        if self.card_counter in self.star_slots:
            kwargs['star_slot'] = True

        next_card = self.cards[self.card_counter]
        success = next_card.play(**kwargs)

        if success:
           self.card_counter += 1
