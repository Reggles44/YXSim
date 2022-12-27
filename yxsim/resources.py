from enum import Enum


class Resource(Enum):
    QI = 1
    DEF = 2
    SWORD_INTENT = 3
    CLOUD_HIT = 4
    INCREASE_ATTACK = 5


    IGNORE_DEFENSE = 101

class Sect(Enum):
    CLOUD = 1
    HEPASTAR = 2
    ELEMENTS = 3


class Job(Enum):
    ELIXIRIST = 1
    FULULIST = 2
    MUSICIAN = 3
    PAINTER = 4
    FORMATION = 5