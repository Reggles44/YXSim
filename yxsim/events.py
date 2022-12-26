import inspect
import typing


class EventManager(dict):
    def add_listener(self, listener: typing.Callable):
        event = inspect.getmro(listener)[1].__name__
        self.setdefault(event, []).append(listener)

    def fire(self, event, **kwargs):
        events = sorted(self.get(event, []), key=lambda event: event.priority)
        map(lambda x: x(**kwargs), events)


class Event:
    def listen(self, **kwargs):
        raise NotImplementedError


class OnSetup(Event):
    '''Triggers when combat has started before any cards are played'''


class OnPlayCard(Event):
    '''Triggers when a card is played'''


class OnAttack(Event):
    '''Triggers when an attack card is played'''


class OnDefend(Event):
    '''Triggers when an attack is recieved'''


class OnResourceGain(Event):
    '''Triggers when a resource is added to the player'''


class OnResourceLoss(Event):
    '''Triggers when a resource is removed from the player'''
