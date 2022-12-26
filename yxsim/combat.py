def combat(*players):
    attacker, defender = sorted(players, key=lambda player: player.cultivation)
    attacker.fire('OnSetup')
    defender.fire('OnSetup')

    while min(attacker.health, defender.health) > 0:
        kwargs = dict(attacker=attacker, defender=defender)
        attacker.play_next_card(**kwargs)

        attacker, defender = defender, attacker



