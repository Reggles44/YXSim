class Card:
    id = ''

    consume = False
    continuous = False

    def play(self, **kwargs) -> bool:
        raise NotImplementedError
