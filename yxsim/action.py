import logging
import typing
from dataclasses import dataclass, field

from yxsim.resources import Resource

logger = logging.getLogger()


@dataclass
class Action:
    # Meta Data
    card_id: str
    source: 'Player'
    target: 'Player' = None
    executed: bool = field(default=False, init=False)
    success: bool = field(default=False, init=False)
    nested: bool = False

    # Input Values
    qi: int = None
    damage: int = None
    healing: int = None
    max_hp_change: int = None
    resource_changes: dict = None
    resource_exhaust: dict = None
    cloud_sword: bool = False
    unrestrained_sword: bool = False

    # Action Nesting
    related_actions: typing.List['Action'] = None
    cloud_hit_action: 'Action' = None
    injured_action: 'Action' = None

    # Measured Results
    damage_to_health: int = field(default=0, init=False)
    effective_healing: int = field(default=0, init=False)

    def any_damage(self):
        return any([
            self.damage,
            self.cloud_hit_action.any_damage(),
            self.injured_action.any_damage(),
            self.related_actions and any([ra.any_damage() for ra in self.related_actions])
        ])

    def execute(self, parent=None) -> 'bool':
        def relative_value(v):
            if isinstance(v, int):
                return v
            else:
                return getattr(parent, v)

        if self.executed:
            raise
        self.executed = True
        logger.debug(self)

        # If we do not have the qi to play this card, do not play it
        if self.qi > self.source.qi:
            self.source.qi += 1
            return False

        if not parent:
            self.source.actions.append(self)

        # TODO do these trigger first or last?
        # parent logic with resources only works right now because it's a prior
        # Iterate over related actions
        for a in self.related_actions:
            a.execute(parent=self)

        # Exhaust before changing
        if self.resource_exhaust:
            for k, v in self.resource_exhaust.items():
                self.source.resources[k] -= relative_value(v)

        # Changing is different than exhausting because we have to track total gained and total spent
        # Track gained and spent as different values, instead of summing into one int
        if self.resource_changes:
            for k, v in self.resource_changes.items():
                if k != Resource.SWORD_INTENT:  # Sword Intent gets modified at the end of the parent execution
                    self.target.resources[k] += v
                    # TODO TRACK GAINED AND SPENT
                elif parent:
                    # Sword Intent is hard because it needs to be added after everything is done
                    # Default confioguration
                    if not self.parent.resource_changes:
                        self.parent.resource_changes = {k:0}
                    elif not k in self.parent.resource_changes:
                        self.parent.resource_changes[k] = 0
                    self.parent.resource_changes[k] += v
                    # TODO TRACK GAINED AND SPENT

        # TODO Set measured results as data is being processed

        if self.damage is not None:
            # Based on the source of the damage, increase damage dealt
            self.damage += self.source.resources.get(Resource.INCREASE_ATTACK) + self.source.resources.get(Resource.SWORD_INTENT)

            # Deal damage to armor first; can't deal more armor damage than there is damage
            armor_damage = min(self.target.armor, self.damage)
            self.target.armor -= armor_damage
            # Overflow damage goes to health
            health_damage = max(0, self.damage - armor_damage)
            # TODO add guard-up calculation here
            self.target.health -= health_damage
            self.damage_to_health = health_damage

            if health_damage:
                if self.injured_action:
                    self.injured_action.execute(parent=self)

        if self.healing > 0:
            self.target.health = min(self.target.max_health)

        if self.cloud_hit_action:
            if self.source.resources.get(Resource.CLOUD_HIT):
                self.cloud_hit_action.execute(parent=self)
            else:
                pass

        self.success = True

        # Resolve end of action configuration changes
        if self.success:
            if not parent:
                if self.damage or self.any_damage():
                    self.source.resources.set(Resource.SWORD_INTENT, 0)

                try:
                    self.target.resources[Resource.SWORD_INTENT] += self.source.resource_changes[Resource.SWORD_INTENT]
                except KeyError:
                    logger.debug('Sword Intent not present in resource changes')
                    pass

                if self.unrestrained_sword:
                    self.source.unrestrained_sword_counter += 1

                # TODO set cloud_hit resolution stuff; make sure that we cant override it to false if there's an infinite cloud hit attribute thing

        return self.executed and self.success
