import inspect
import logging
import typing

logger = logging.getLogger()


class Event:
    def __init__(self, source_card, priority=0):
        self.source_card = source_card
        self.priority = priority

    def handle(self, **kwargs):
        raise NotImplementedError


class EventManager(dict):
    def add_listener(self, listener: Event):
        event = inspect.getmro(listener.__class__)[1].__name__
        self.setdefault(event, []).append(listener)
        logger.debug(f'{getattr(self, "id", "EventManager")} adding listener {listener.__class__.__name__} for event {event}')

    def fire(self, event, **kwargs):
        logger.debug(f'{getattr(self, "id", "EventManager")} firing {event} with kwargs {kwargs}')
        events = sorted(self.get(event, []), key=lambda event: event.priority)
        logger.debug(f'{getattr(self, "id", "EventManager")} has handlers {events}')
        for evt in events:
            evt.handle(**kwargs)


class OnSetup(Event):
    '''Triggers when combat has started before any cards are played'''


class OnPlayCard(Event):
    '''Triggers when a card is played'''


class OnChangeHealth(Event):
    '''Triggers when current health changes (goes up, goes down)'''


class OnAttack(Event):
    '''Triggers when an attack card is played'''


class OnDefend(Event):
    '''Triggers when an attack is recieved'''


class OnResourceGain(Event):
    '''Triggers when a resource is added to the player'''


class OnResourceLoss(Event):
    '''Triggers when a resource is removed from the player'''
