import math
from typing import List
from typing import Tuple


def ms_to_s(ms: int) -> float:
    return ms / 1000.0


def deg_to_rad(deg: float) -> float:
    return deg * (math.pi / 180.0)


def kph_to_mps(kph: float) -> float:
    return kph / 3.6


def mps_to_kph(mps: float) -> float:
    return mps * 3.6


def move_point(cx: float, cy: float, x: float, y: float) -> Tuple[float, float]:
    return x + cx, y + cy


def rotate_point(
    theta: float, cx: float, cy: float, x: float, y: float
) -> Tuple[float, float]:
    x, y = move_point(-cx, -cy, x, y)

    c = math.cos(theta)
    s = math.sin(theta)

    x_s = x * c - y * s
    y_s = x * s + y * c

    x_s, y_s = move_point(cx, cy, x_s, y_s)

    return x_s, y_s


def compute_velocities(
    long_velocities_mps: List[float], lat_velocities_mps: List[float]
) -> List[float]:
    return [
        math.sqrt(v_long**2 + v_lat**2)
        for v_long, v_lat in zip(long_velocities_mps, lat_velocities_mps)
    ]


def compute_heading_degrees(
    long_velocities_mps: List[float], lat_velocities_mps: List[float]
) -> List[float]:
    return [
        (math.atan2(v_lat, v_long) / math.pi) * 180.0
        for v_long, v_lat in zip(long_velocities_mps, lat_velocities_mps)
    ]


def compute_accelerations(
    velocities_mps: List[float], time_span_ms: int
) -> List[float]:
    accelerations_mps2 = [0.0]
    for i in range(1, len(velocities_mps)):
        accelerations_mps2.append(
            (velocities_mps[i] - velocities_mps[i - 1]) / time_span_ms
        )
    return accelerations_mps2


def compute_rel_velocities(
    velocities_mps: List[float], ego_velocities_mps: List[float]
) -> List[float]:
    return [
        v_ego - v_veh
        for v_veh, v_ego in zip(velocities_mps, ego_velocities_mps)
    ]


def compute_rel_accelerations(
    accelerations_mps2: List[float], ego_accelerations_mps2: List[float]
) -> List[float]:
    return [
        a_ego - a_veh
        for a_veh, a_ego in zip(accelerations_mps2, ego_accelerations_mps2)
    ]
