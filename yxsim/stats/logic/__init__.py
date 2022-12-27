import logging
import pkgutil

logger = logging.getLogger()


class Registry(dict):
    def __getitem__(self, item):
        if item and item not in self:
            self.register(item)

        return self.get(item)()

    def register(self, item):
        if item in self:
            logger.debug(f'{item} already registered')
            return
        obj = __import__(item, globals(), locals(), ['StatType'], 1).StatType
        self[item] = obj
        logger.debug(f'Registered {item} - {obj}')

    def autoregister(self):
        map(self.register, (name for _, name, _ in pkgutil.iter_modules(__path__)))


registry = Registry()