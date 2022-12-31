import logging
from yxsim.resources import Resource

logger = logging.getLogger()


def combat(p1, p2, limit=64):
    attacker, defender = sorted([p1, p2], key=lambda player: player.cultivation, reverse=True)
    attacker.fire('OnSetup')
    defender.fire('OnSetup')

    turn = 0
    while min(attacker.health, defender.health) > 0 and turn < limit:
        logger.debug(f'Turn {turn}\t{attacker.id}({attacker.health}) is attacking {defender.id}({defender.health})')
        kwargs = dict(attacker=attacker, defender=defender)
        if attacker.resources[Resource.STATIC_DEF] > 0:
            attacker.resources[Resource.STATIC_DEF] -= 1
        else:
            attacker.resources[Resource.DEF] //= 2

        attacker.play_next_card(**kwargs)

        attacker, defender = defender, attacker
        turn += 1

    return sorted([p1, p2], key=lambda player: player.health)
