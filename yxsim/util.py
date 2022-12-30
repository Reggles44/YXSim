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
            source.resources[Resource.SPENT_HEXAGRAM] += 1
            return self.max

        random_setting = source.random_setting
        if random_setting == 'mean':
            return (self.min + self.max) // 2
        elif random_setting == 'rand':
            return random.randint(self.min, self.max)
        else:
            return None


def random_chance(n, chance, source):
    results = 0

    consumed_hexagram = min(n, source.resources[Resource.HEXAGRAM])
    n -= consumed_hexagram
    source.resources[Resource.HEXAGRAM] -= consumed_hexagram
    source.resources[Resource.SPENT_HEXAGRAM] += consumed_hexagram
    results += consumed_hexagram

    if not n:
        return results

    random_setting = source.random_setting
    if random_setting == 'mean':
        results += (n*chance)//1
    elif random_setting == 'rand':
        for _ in range(n):
            if random.random() < chance:
                results += 1

    return int(results)


def debuffs(source):
    available_debuffs = list(filter(lambda d: source.resources[d] > 0, set(source.resources.keys()) & set(Resource.debuffs())))
    return available_debuffs


def has_debuffs(source):
    return bool(debuffs(source))