import typing
import inspect


class ReferenceValue:
    def __init__(self, callable: typing.Callable, *args, **kwargs):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def cast(self, *args, **kwargs):
        callable_signature = inspect.signature(self.callable)
        kwargs = {k: v for k, v in {**self.kwargs, **kwargs}.items() if k in callable_signature.parameters}
        return self.callable(*args, *self.args, **kwargs)