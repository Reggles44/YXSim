import logging

from yxsim.characters.base import Character

logger = logging.getLogger(__name__)

logic_path = __path__


class Registry(dict):
    cls_name = 'CharacterType'

    def __getitem__(self, item):
        if item and item not in self:
            character = __import__(item, globals(), locals(), [self.cls_name], 1)
            print(character)
            self.register(item, getattr(character, self.cls_name))

        return self.get(item, Character)

    def register(self, name, character):
        assert name not in self, name
        self[name] = character
        logger.debug(f'Registered {name} - {character}')


registry = Registry()
