import logging
import pkgutil


logger = logging.getLogger()


class Registry(dict):
    def __getitem__(self, item):
        if item and item not in self:
            self.register(item)

        return self.get(item, self.get('normal_attack'))()

    def register(self, item):
        if item in self:
            logger.debug(f'{item} already registered')
            return
        logger.debug(f'{item} registering')
        obj = __import__(item, globals(), locals(), ['CardType'], 1).CardType
        obj.id = item
        self[item] = obj
        logger.debug(f'Registered {item} - {obj}')

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(__path__):
            print(name)
            self.register(name)


registry = Registry()
registry.register('normal_attack')
