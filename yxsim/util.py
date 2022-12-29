import random
import typing
import inspect

from yxsim.resources import Resource


class ReferenceValue:
    def __init__(self, callable: typing.Callable, *args, **kwargs):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def cast(self, *args, **kwargs):
        callable_signature = inspect.signature(self.callable)
        kwargs = {k: v for k, v in {**self.kwargs, **kwargs}.items() if k in callable_signature.parameters}
        return self.callable(*args, *self.args, **kwargs)


class RandomValue:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def cast(self, source: 'Player', **kwargs):
        if source.resources[Resource.HEXAGRAM] > 0:
            source.resources[Resource.HEXAGRAM] -= 1
            return self.max

        random_setting = source.random_setting
        if random_setting == 'mean':
            return (self.min + self.max) // 2
        elif random_setting == 'rand':
            return random.randint(self.min, self.max)
        else:
            return None
