import sys

import pytest

from yxsim.resources import Job

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


card_names = [card.display_name for card in card_registry.values()]
@pytest.mark.parametrize('card', card_registry.values(), ids=card_registry.keys())
def test_duplicate_name(card):
    if card_names.count(card.display_name) > 1:
        raise ValueError(f'Invalid display_name for {card}')



@pytest.mark.parametrize('job', Job)
@pytest.mark.skip
def test_job_coverage(job):

    coverage_dict = {}
    for card in card_registry.values():
        if card.job == job:
            coverage_dict.setdefault(card.phase, []).append(card)

    assert len(coverage_dict) == 15
    assert coverage_dict[1] == 6
    assert coverage_dict[2] == 3
    assert coverage_dict[3] == 3
    assert coverage_dict[4] == 3