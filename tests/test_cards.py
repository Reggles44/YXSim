import sys

import pytest

MODULE = sys.modules[__name__]


from yxsim.cards.logic import registry as card_registry
for card_name, card in card_registry.items():
    test_dict = card()._test()

    @pytest.mark.parametrize('func', test_dict.values(), ids=test_dict.keys())
    def run(func):
        func()

    setattr(MODULE, f'test_{card_name}', run)


def test_if_tests_exist():
    base_tests = ['test_if_tests_exist', 'test_duplicate_name']
    dynamic_tests = [var for var in dir(MODULE) if var.startswith('test_') and var not in base_tests]
    assert len(dynamic_tests) > 0, dynamic_tests


