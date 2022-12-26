import logging
import typing
from dataclasses import dataclass

from yxsim.resources import Resource

logger = logging.getLogger()


@dataclass
class Action:
    source: 'Player'
    target: 'Player' = None
    executed = False

    damage: int = 0
    healing: int = 0
    effective_healing: int = 0
    increase_max_hp: int = 0
    decrease_max_hp: int = 0
    resource_changes: dict = None

    # Action Nesting
    related_actions: typing.List['Action'] = None
    cloud_hit_action: 'Action' = None

    def execute(self):
        if self.executed:
            return
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




