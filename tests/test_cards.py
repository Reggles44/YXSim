import os

import pytest

from yxsim.cards.logic import registry as card_registry

card_logic_path = os.path.join(os.getcwd(), 'yxsim', 'cards', 'logic')


@pytest.mark.parametrize('name, card', card_registry.items())
def test_card(name, card):
    try:
        card = card_registry[name]
        card.test()
    except NotImplementedError:
        raise



# TODO
# test holding sword intent
