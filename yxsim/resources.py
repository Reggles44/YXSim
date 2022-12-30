from enum import Enum


class Resource(Enum):
    QI = 1
    DEF = 2
    SWORD_INTENT = 3
    INCREASE_ATTACK = 5
    UNRESTRAINED_SWORD_COUNTER = 6
    CLOUD_HIT_COUNTER = 7
    GUARD_UP = 8
    PLAY_TWICE = 9
    SPIRIT_SWORD_DISCOUNT = 10
    HEXAGRAM = 11
    IGNORE_DEF = 12
    STATIC_DEF = 13
    STAR_POWER = 14

    CHASE_BLOCKED = 90
    QI_COST_REDUCTION = 91
    SPENT_HEXAGRAM = 92
    TOTAL_HEALING = 93

    INTERNAL_INJURY = 101
    FLAW = 102
    WEAKENED = 103

    @classmethod
    def debuffs(cls) -> list:
        return [res for res in cls if res.value > 100]


class Sect(Enum):
    CLOUD = 1
    HEPTASTAR = 2
    ELEMENTS = 3


class Job(Enum):
    ELIXIRIST = 1
    FULULIST = 2
    MUSICIAN = 3
    PAINTER = 4
    FORMATION = 5

class Direction(Enum):
    Right = 1
    Left = 2