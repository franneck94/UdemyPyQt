from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List


class LaneAssociationType(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    NONE = auto()


class ObjectClassType(Enum):
    CAR = auto()
    TRUCK = auto()
    MOTORBIKE = auto()
    NONE = auto()


@dataclass
class VehicleInformationType:
    id: int
    object_class: ObjectClassType
    width_m: float
    height_m: float

    lane: LaneAssociationType
    velocity_mps: float
    long_distance_m: float
    lat_distance_m: float


NeighborVehiclesType = List[VehicleInformationType]


@dataclass
class Polynomial3rdDegreeType:
    a: float
    b: float
    c: float
    d: float

    def __call__(self, x: float) -> float:
        return self.a**3 * x + self.b**2 * x + self.c * x + self.d


class LaneBoundaryType(Enum):
    DASHED = auto()
    SOLID = auto()
    NONE = auto()


class LaneClassType(Enum):
    NORMAL = auto()
    ACCELERATION = auto()
    DECELERATION = auto()
    HARD_SHOULDER = auto()
    NONE = auto()


@dataclass
class LaneInformationType:
    left_polynomial: Polynomial3rdDegreeType
    right_polynomial: Polynomial3rdDegreeType

    left_boundary_type: LaneBoundaryType
    right_boundary_type: LaneBoundaryType

    left_view_range_m: float
    right_view_range_m: float

    lane_width_m: float
    lane_class: LaneClassType


@dataclass
class LanesInformationType:
    left_lane: LaneInformationType
    center_lane: LaneInformationType
    right_lane: LaneInformationType
