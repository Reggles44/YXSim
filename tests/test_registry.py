import pytest
from yxsim.resources import Job
from yxsim.cards.logic import registry as card_registry


card_names = [card.display_name for card in card_registry.values()]
@pytest.mark.parametrize('card', card_registry.values(), ids=card_registry.keys())
def test_duplicate_name(card):
    if card_names.count(card.display_name) > 1:
        raise ValueError(f'Invalid display_name for {card}')


@pytest.mark.parametrize('job', Job)
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