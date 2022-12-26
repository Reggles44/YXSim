import logging

from yxsim.destinies.base import Destiny

logger = logging.getLogger(__name__)

logic_path = __path__


class Registry(dict):
    cls_name = 'DestinyType'

    def __getitem__(self, item):
        if item not in self:
            character = __import__(item, globals(), locals(), [self.cls_name], 1)
            self.register(item, getattr(character, self.cls_name))

        return self.get(item, Destiny)

    def register(self, name, character):
        assert name not in self, name
        self[name] = character
        logger.debug(f'Registered {name} - {character}')


registry = Registry()
