import dataclasses
import logging
import typing
from dataclasses import dataclass, field, fields

from yxsim.resources import Resource

logger = logging.getLogger()


@dataclass
class Action:
    # Meta Data
    card: 'CardType'
    source: 'Player' = field(repr=False)
    target: 'Player' = field(default=None, repr=False)
    executed: bool = field(default=False, init=False)
    success: bool = field(default=False, init=False)
    parent: 'Action' = None

    # Input Values
    event: bool = False
    chase: bool = field(default=False, init=True, metadata={'input': True})
    damage: int = field(default=None, metadata={'input': True})
    ignore_armor: bool = field(default=False, metadata={'input': True})  # For things like Ice Fulu
    healing: int = field(default=None, metadata={'input': True})
    max_hp_change: int = field(default=None, metadata={'input': True})
    resource_changes: dict = field(default=None, metadata={'input': True})
    resource_exhaust: dict = field(default=None, metadata={'input': True})

    # Action Nesting
    related_actions: list['Action'] = None
    cloud_hit_action: 'Action' = None
    injured_action: 'Action' = None

    # Utility
    sword_intent_buffer: list = None

    # Measured Results
    damage_to_health: int = field(default=0, init=False)
    effective_healing: int = field(default=0, init=False)

    def execute(self, parent=None) -> 'bool':
        if self.sword_intent_buffer is None:
            self.sword_intent_buffer = list()

        # Execution lock so we never execute the same action twice
        if self.executed:
            raise
        self.executed = True

        # Logging and setting Parent for any child action
        if not parent:
            self.source.actions.append(self)
            logger.info(f'Executing action for {self.card.id}: {self}')
        else:
            self.parent = parent
            logger.debug(f'Executing child action {self.card.id}: {self}')

        # If we do not have the qi to play this card, do not play it
        if not parent and not self.card.free and not self.event:
            qi = getattr(self.card, 'qi')
            # Spirit swords can be discounted
            if self.card.spirit_sword:
                qi = max(qi - max(0, self.source.resources[Resource.SPIRIT_SWORD_DISCOUNT]), 0)

            if qi is not None and qi:
                player_qi = self.source.resources[Resource.QI]
                if qi > player_qi:
                    logger.info(f'Could not afford {self.card}; gaining 1 qi instead')
                    self.source.resources[Resource.QI] += 1
                    return self
                else:
                    logger.debug(f'Spending {qi} qi from a reserve of {self.source.resources[Resource.QI]}')
                    self.source.resources[Resource.QI] -= qi

        # Convert all of our `ReferenceValue` and `RandomValue` to values
        for field in filter(lambda f: f.metadata.get('input'), fields(self)):
            attr = getattr(self, field.name)
            try:
                setattr(self, field.name, attr.cast(**self.__dict__))
            except AttributeError as e:
                pass

        # TODO do these trigger first or last?
        # parent logic with resources only works right now because it's a prior
        # Iterate over related actions
        for a in self.related_actions or []:
            a.execute(parent=self)

        # Exhaust before changing
        if self.resource_exhaust:
            for k, v in self.resource_exhaust.items():
                logger.debug(f'Resource {k} starting at {self.source.resources[k]} decreasing by {v}')
                self.source.resources[k] = max(self.source.resources[k]-v, 0)

        # Changing is different than exhausting because we have to track total gained and total spent
        # Track gained and spent as different values, instead of summing into one int
        if self.resource_changes:
            for k, v in self.resource_changes.items():
                if k == Resource.SWORD_INTENT:
                    logger.debug(f'Sword Intent starting at {self.source.resources[k]} increasing by {v}')
                    self.sword_intent_buffer.append((self.target, v))
                else:
                    logger.debug(f'Resource {k} starting at {self.source.resources[k]} increasing by {v}')
                    self.target.resources[k] += v
                    self.target.resources[k] = max(self.target.resources[k], 0)

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
            if self.source.cloud_hit_active or self.source.resources.get(Resource.CLOUD_HIT_COUNTER):
                self.cloud_hit_action.execute(parent=self)
            else:
                pass

        self.success = True

        # Resolve end of action configuration changes
        if self.success:
            if parent:
                self.parent.sword_intent_buffer.extend(self.sword_intent_buffer)
            else:
                # Reset sword intent
                if self.damage or self.any_damage():
                    logger.debug(f'Reducing Sword Intent to zero')
                    self.source.resources[Resource.SWORD_INTENT] = 0

                # Apply sword intent buffer
                for _t, v in self.sword_intent_buffer:
                    logger.debug(f'Increasing sword intent by {v} for {_t}')
                    _t.resources[Resource.SWORD_INTENT] = max(0, _t.resources[Resource.SWORD_INTENT]+v)
                self.sword_intent_buffer = list()

                # Calculate Cloud Sword
                cloud_sword = getattr(self.card, 'cloud_sword')
                if cloud_sword is not None and cloud_sword:
                    self.source.resources[Resource.CLOUD_HIT_COUNTER] += 1
                else:
                    self.source.resources[Resource.CLOUD_HIT_COUNTER] = 0

                # Calculate Unrestrained Sword
                unrestrained_sword = getattr(self.card, 'unrestrained_sword')
                if unrestrained_sword is not None and unrestrained_sword:
                    self.source.resources[Resource.UNRESTRAINED_SWORD_COUNTER] += 1

        return self

    def any_damage(self):
        return any([
            self.success and self.damage,
            self.cloud_hit_action and self.cloud_hit_action.success and self.cloud_hit_action.any_damage(),
            self.injured_action and self.injured_action.success and self.injured_action.any_damage(),
            self.related_actions and any([ra.success and ra.any_damage() for ra in self.related_actions])
        ])

    def any_chase(self):
        return any([
            self.success and self.chase,
            self.cloud_hit_action and self.cloud_hit_action.success and self.cloud_hit_action.any_chase(),
            self.injured_action and self.injured_action.success and self.injured_action.any_chase(),
            self.related_actions and any([ra.success and ra.any_chase() for ra in self.related_actions])
        ])
