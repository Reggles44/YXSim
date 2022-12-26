import logging
import typing
from dataclasses import dataclass, field

from yxsim.resources import Resource

logger = logging.getLogger()


@dataclass
class Action:
    source: 'Player'
    target: 'Player' = None
    executed: bool = field(default=False, init=False)
    success: bool = field(default=False, init=False)

    # Input Values
    damage: int = 0
    healing: int = 0
    max_hp_change: int = 0
    resource_changes: dict = None

    # Action Nesting
    related_actions: typing.List['Action'] = None
    cloud_hit_action: 'Action' = None
    injured_action: 'Action' = None

    # Measured Results
    damage_to_health: int = field(default=0, init=False)
    effective_healing: int = field(default=0, init=False)

    def execute(self) -> 'bool':
        if self.executed:
            raise
        self.executed = True
        logger.debug(self)

        if self.damage > 0:
            self.target.health -= self.damage

        if self.healing > 0:
            self.target.health = min(self.target.max_health)

        if self.cloud_hit_action:
            if self.source.resources.get(Resource.CLOUD_HIT):
                self.cloud_hit_action.execute()
            else:
                self.source.resources

        return self.executed and self.success

    @property
    def injured(self) -> bool:
        return self.damage_to_health > 0



