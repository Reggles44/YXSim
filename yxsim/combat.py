import logging

logger = logging.getLogger()


def combat(p1, p2, limit=64):
    attacker, defender = sorted([p1, p2], key=lambda player: player.cultivation)
    attacker.fire('OnSetup')
    defender.fire('OnSetup')

    turn = 0
    while min(attacker.health, defender.health) > 0 and turn < limit:
        logger.debug(f'Turn {turn}\t{attacker.id} is attacking {defender.id}')
        kwargs = dict(attacker=attacker, defender=defender)
        attacker.play_next_card(**kwargs)

        attacker, defender = defender, attacker
        turn += 1

    return sorted([p1, p2], key=lambda player: player.health)
