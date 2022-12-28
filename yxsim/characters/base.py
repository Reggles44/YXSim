class Character:
    id = None
    display_name = ''

    def setup(self, attacker, defender):
        raise NotImplementedError

    def __str__(self):
        self.__repr__()

    def __repr__(self):
        return self.display_name