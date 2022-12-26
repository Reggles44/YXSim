from yxsim.combat import combat
from yxsim.player import Player
from yxsim.config import configure_logging

combat_data = {
    'PLAYER': {
        'max_health': 100,
        'character': '',
        'destinies': [],
        'cards': [
            'cloud_sword_touch_sky',
            'cloud_sword_fleche',
            'cloud_sword_touch_earth',
            'light_sword',
            'giant_tiger_spirit_sword'
        ],
        'slots': 8,
        'star_slots': [],
        'cultivation': 10
    },
    'ENEMY': {
        'character': '',
        'destinies': [],
        'cards': [],
        'slots': 8,
        'star_slots': [],
        'cultivation': 10
    }
}

if __name__ == '__main__':
    configure_logging()
    combat(*[Player(**pdata) for pdata in combat_data.values()])