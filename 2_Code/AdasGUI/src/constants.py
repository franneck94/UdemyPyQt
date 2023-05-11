from typing import Final


LANE_NAMES = ("Left", "Center", "Right", "None")

OBJECT_NAMES = ("Car", "Truck", "Motorbike", "None")

EGO_VEHICLE_ID: Final[int] = -1
NONE_VEHICLE_ID: Final[int] = -2
MAX_NUM_VEHICLES: Final[int] = 6
LONGITUDINAL_DIFFERENCE_PERCENTAGE: Final[float] = 0.05
NUM_LANES: Final[int] = 3

EGO_VEHICLE_WIDTH_M: Final[float] = 2.5
EGO_VEHICLE_HEIGHT_M: Final[float] = 5.0

CYCLE_TIME_MS: Final[int] = 50


def ms_to_s(ms: int) -> float:
    return ms / 1000.0


CYCLE_TIME_S: Final[float] = ms_to_s(CYCLE_TIME_MS)
