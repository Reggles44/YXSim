import logging
import pkgutil

from yxsim.characters.base import Character

logger = logging.getLogger()


class Registry(dict):
    def __getitem__(self, item):
        if item and item not in self:
            self.register(item)

        return self.get(item, Character)()

    def register(self, item):
        if item in self:
            logger.debug(f'{item} already registered')
            return
        obj = __import__(item, globals(), locals(), ['CharacterType'], 1).CharacterType
        self[item] = obj
        logger.debug(f'Registered {item} - {obj}')

    def autoregister(self):
        map(self.register, (name for _, name, _ in pkgutil.iter_modules(__path__)))


registry = Registry()
