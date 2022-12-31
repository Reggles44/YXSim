import inspect
import logging
import typing

logger = logging.getLogger()


class Event:
    def __init__(self, source, source_card, continuous=None, priority=0):
        self.source = source
        self.source_card = source_card
        self.continuous = continuous
        self.priority = priority
        self.enabled = True

    def handle(self, **kwargs):
        raise NotImplementedError


class EventManager(dict):
    def add_listener(self, listener: Event):
        event = inspect.getmro(listener.__class__)[1].__name__
        self.setdefault(event, []).append(listener)
        logger.debug(f'{getattr(self, "id", "EventManager")} adding listener {listener.__class__.__name__} for event {event}')

    def remove_listener(self, listener):
        event = inspect.getmro(listener.__class__)[1].__name__
        if event in self and listener in self[event]:
            self[event].remove(listener)
            logger.debug(f'{getattr(self, "id", "EventManager")} removing listener {listener.__class__.__name__} for event {event}')

    def fire(self, event, **kwargs):
        logger.debug(f'{getattr(self, "id", "EventManager")} firing {event} with kwargs {kwargs}')
        events = sorted(self.get(event, []), key=lambda event: event.priority)
        logger.debug(f'{getattr(self, "id", "EventManager")} has handlers {events}')
        for evt in events:
            if evt.enabled:
                evt.handle(**kwargs)

                # Limited Continuous Logic
                if isinstance(evt.continuous, int):
                    evt.continuous -= 1
                    if evt.continuous <= 0:
                        self.remove_listener(evt)



class OnSetup(Event):
    '''Triggers when combat has started before any cards are played'''


class OnPlayCard(Event):
    '''Triggers when a card is played'''


class OnChangeHealth(Event):
    '''Triggers when current health changes (goes up, goes down)'''


class OnInjure(Event):
    '''Triggers when an Injure is occurred'''


class OnAttack(Event):
    '''Triggers when an attack card is played'''


class OnDefend(Event):
    '''Triggers when an attack is recieved'''


class OnResourceGain(Event):
    '''Triggers when a resource is added to the player'''


class OnResourceLoss(Event):
    '''Triggers when a resource is removed from the player'''


class OnTurnStart(Event):
    '''Triggers on start of turn'''


class OnTurnEnd(Event):
    '''Triggers on start of turn'''