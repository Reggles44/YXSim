import logging
import typing
from dataclasses import dataclass, field

from yxsim.resources import Resource

logger = logging.getLogger()


@dataclass
class Action:
    # Meta Data
    card: 'CardType'
    source: 'Player'
    target: 'Player' = None
    executed: bool = field(default=False, init=False)
    success: bool = field(default=False, init=False)
    nested: bool = False

    # Input Values
    damage: int = None
    ignore_armor: bool = False  # For things like Ice Fulu
    healing: int = None
    max_hp_change: int = None
    resource_changes: dict = None
    resource_exhaust: dict = None

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
            self.cloud_hit_action and self.cloud_hit_action.any_damage(),
            self.injured_action and self.injured_action.any_damage(),
            self.related_actions and any([ra.any_damage() for ra in self.related_actions])
        ])

    def execute(self, parent=None) -> 'bool':
        for property in ['damage', 'ignore_armor', 'healing', 'max_hp_change', 'resource_changes', 'resource_exhaust']:
            attr = getattr(self, property)
            try:
                setattr(self, property, attr.cast())
            except AttributeError:
                pass

        if not parent:
            logger.info(f'Executing event for {self.card.id}: {self}')
        else:
            logger.debug(f'Executing child event {self.card.id}: {self}')

        def relative_value(v):
            if isinstance(v, int):
                return v
            else:
                return getattr(parent, v)

        if self.executed:
            raise
        self.executed = True

        # If we do not have the qi to play this card, do not play it
        qi = getattr(self.card, 'qi')
        if qi is not None and qi:
            player_qi = self.source.resources[Resource.QI]
            if qi > player_qi:
                logger.info(f'Could not afford {self.card}; gaining 1 qi instead')
                self.source.resources[Resource.QI] += 1
                return False
            else:
                logger.debug(f'Spending {qi} qi from a reserve of {self.source.resources[Resource.QI]}')
                self.source.resources[Resource.QI] -= qi

        if not parent:
            self.source.actions.append(self)

        # TODO do these trigger first or last?
        # parent logic with resources only works right now because it's a prior
        # Iterate over related actions
        for a in self.related_actions or []:
            a.execute(parent=self)

        # Exhaust before changing
        if self.resource_exhaust:
            for k, v in self.resource_exhaust.items():
                v = relative_value(v)
                logger.debug(f'Resource {k} starting at self.source.resources[k] decreasing by {v}')
                self.source.resources[k] -= v

        # Changing is different than exhausting because we have to track total gained and total spent
        # Track gained and spent as different values, instead of summing into one int
        if self.resource_changes:
            for k, v in self.resource_changes.items():
                if k != Resource.SWORD_INTENT:  # Sword Intent gets modified at the end of the parent execution
                    v = relative_value(v)
                    logger.debug(f'Resource {k} starting at self.source.resources[k] increasing by {v}')
                    self.target.resources[k] += v

                    # TODO TRACK GAINED AND SPENT
                elif parent:
                    # Sword Intent is hard because it needs to be added after everything is done
                    # Default confioguration
                    if not self.parent.resource_changes:
                        self.parent.resource_changes = {k:0}
                    elif not k in self.parent.resource_changes:
                        self.parent.resource_changes[k] = 0
                    logger.debug(f'Resource {k} starting at self.source.resources[k] increasing by {v}')
                    self.parent.resource_changes[k] += v
                    # TODO TRACK GAINED AND SPENT


        if self.damage is not None:
            self.effective_damage = 0

            # Based on the source of the damage, increase damage dealt
            damage = self.damage + int(self.source.resources[Resource.INCREASE_ATTACK]) + int(self.source.resources[Resource.SWORD_INTENT])
            if damage:
                if damage != self.damage:
                    logger.debug(f'Recalculated damage is {damage}')

                # Deal damage to armor first; can't deal more armor damage than there is damage
                if self.ignore_armor:
                    logger.debug(f'Ignoring armor as an intrinsic property of the damage being dealt')
                    armor_damage = 0
                elif self.source.resources[Resource.IGNORE_DEF] > 0:
                    logger.debug('Ignoring armor by consuming IGNORE DEFENSE')
                    self.source.resources[Resource.IGNORE_DEF] -= 1
                    armor_damage = 0
                else:
                    armor_damage = min(self.target.resources[Resource.DEF], damage)
                    if armor_damage:
                        logger.info(f'Dealing {armor_damage} to armor')
                        self.target.resources[Resource.DEF] -= armor_damage
                        self.effective_damage += armor_damage

                # Overflow damage goes to health
                health_damage = max(0, damage - armor_damage)
                if health_damage:
                    if self.target.resources[Resource.GUARD_UP] > 0:
                        logger.info(f'Consuming one of {self.target.resources[Resource.GUARD_UP]} of guard-up')
                        self.target.resources[Resource.GUARD_UP] -= 1
                        self.damage_to_health = 0
                    else:
                        logger.info(f'Dealing {health_damage} to health')
                        self.target.health -= health_damage
                        self.damage_to_health = health_damage
                        self.effective_damage += health_damage

                if health_damage:
                    if self.injured_action:
                        self.injured_action.execute(parent=self)

        if self.max_hp_change is not None:
            self.target.max_health = max(0, self.target.max_health + self.max_hp_change)  # TODO do we track this as damage or something

        if self.healing and self.healing > 0:
            max_healing = self.target.max_health - self.target.health
            effective_healing = min(self.healing, max_healing)
            self.target.health += effective_healing
            self.effective_healing = effective_healing

        if self.cloud_hit_action:
            if self.source.cloud_hit_active or self.source.resources.get(Resource.CLOUD_HIT):
                self.cloud_hit_action.execute(parent=self)
            else:
                pass

        self.success = True

        # Resolve end of action configuration changes
        if self.success:
            if not parent:
                if self.damage or self.any_damage():
                    self.source.resources[Resource.SWORD_INTENT] = 0

                try:
                    self.target.resources[Resource.SWORD_INTENT] += self.resource_changes[Resource.SWORD_INTENT]
                except KeyError:
                    logger.debug('Sword Intent not present in resource changes')
                except TypeError:
                    logger.debug('Resource changes not defined on action')

                cloud_sword = getattr(self.card, 'cloud_sword')
                if cloud_sword is not None and cloud_sword:
                    self.source.resources[Resource.CLOUD_HIT] += 1
                else:
                    self.source.resources[Resource.CLOUD_HIT] = 0

                unrestrained_sword = getattr(self.card, 'unrestrained_sword')
                if unrestrained_sword is not None and unrestrained_sword:
                    self.source.unrestrained_sword_counter += 1


        return self.executed and self.success
