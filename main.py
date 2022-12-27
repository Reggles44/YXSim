from yxsim.combat import combat
from yxsim.player import Player
from yxsim.config import configure_logging

combat_data = {
    'PLAYER': {
        'max_health': 100,
        'cultivation': 1,
        'slots': 5,

        'character': '',
        'destinies': [],
        'cards': [
            'cloud_sword_touch_sky',
            'cloud_sword_fleche',
            'cloud_sword_touch_earth',
            'light_sword',
            'giant_tiger_spirit_sword'
        ],
        'star_slots': [],
    },
    'ENEMY': {
        'max_health': 100,
        'cultivation': 1,
        'slots': 5,

        'character': '',
        'destinies': [],
        'cards': [],
        'star_slots': [],
    }
}

if __name__ == '__main__':
    configure_logging()
    combat(*[Player(id=id, **pdata) for id, pdata in combat_data.items()])