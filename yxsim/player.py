import collections
import logging

from yxsim.cards.logic import registry as card_registry
from yxsim.characters.logic import registry as character_registry
from yxsim.destinies.logic import registry as destiny_registry
from yxsim.events import EventManager
from yxsim.resources import Resource, Direction

logger = logging.getLogger()


class Player(EventManager):
    def __init__(
            self,
            id,
            cards,

            max_health=100,
            cultivation=0,
            slots=8,
            character=None,
            destinies=None,
            star_slots=None,
    ):
        super().__init__()
        self.id = id

        self.resources = collections.defaultdict(int)
        self.actions = []

        self.health = max_health
        self.max_health = max_health
        self.cultivation = cultivation
        self.slots = slots

        self.character = character_registry[character]

        for destiny in destinies or []:
            self.add_listener(destiny_registry[destiny])

        self.cards = []
        self.cards = [card_registry[cards[i] if i < len(cards) else ''] for i in range(slots)]
        self.direction = Direction.Right
        self.star_slots = star_slots or []
        self.card_counter = 0
        self.cloud_hit_active = False  # Whether cloud hit is permanently active

        logger.debug(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'''Player ({', '.join([f'{name}={getattr(self, name).__repr__()}' for name in vars(self)])})'''

    def play_next_card(self, **kwargs):
        chase = kwargs.get('chase', False)
        logger.debug(f'Next play slot is {self.card_counter}')

        if self.card_counter in self.star_slots:
            kwargs['star_slot'] = True

        next_card = self.cards[self.card_counter]
        logger.debug(f'{self.id} playing {next_card}')

        actions = []
        action = next_card._play(**kwargs)
        actions.append(action)
        if self.resources[Resource.PLAY_TWICE] > 0:
            action = next_card._play(free=True, **kwargs)
            actions.append(action)
            self.resources[Resource.PLAY_TWICE] -= 1

        self.fire('OnPlayCard', card=next_card, **kwargs)

        if any([a.success for a in actions]):
            # For Hunting Hunting Hunter
            if self.direction == Direction.Right:
                incr = 1
            else:
                incr = -1

            # Discover next card
            # Pass over exhausted ones
            n = 6
            for e in range(n):
                self.card_counter += incr
                self.card_counter %= 7
                if not self.cards[self.card_counter].exhausted:
                    break
                if e == n-1:
                    raise ValueError(f'No valid cards to play')

        if any([a.any_chase() for a in actions]) and not chase:
            self.play_next_card(chase=True, **kwargs)
