class ReferenceValue:
    def __init__(self, some_callable, *args, **kwargs):
        self.some_callable = some_callable
        self.args = args
        self.kwargs = kwargs

    def cast(self):
        return self.some_callable(*self.args, **self.kwargs)