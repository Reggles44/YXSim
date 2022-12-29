import sys

MODULE = sys.modules[__name__]


from yxsim.cards.logic import registry as card_registry
for card_name, card in card_registry.items():
    for test_name, func in card()._test():
        setattr(MODULE, f'test_{card_name}_{test_name}', lambda: func())


def test_if_tests_exist():
    assert any(var.startswith('test_') for var in dir(MODULE))
