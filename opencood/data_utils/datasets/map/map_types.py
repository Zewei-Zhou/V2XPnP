import dataclasses
from enum import IntEnum
from typing import List, Union

# basic
@dataclasses.dataclass
class MapPoint:
    x: float
    y: float
    z: float

@dataclasses.dataclass
class TrafficSignalLaneState:
    lane: int
    state: str

@dataclasses.dataclass
class DynamicState:
    timestamp_seconds: float
    lane_states: List[TrafficSignalLaneState]

class LaneType(IntEnum):
    Unknown = 0
    Driving = 1
    Sidewalk = 2
    Shoulder = 3
    ParkingLane = 4


# static objects
@dataclasses.dataclass
class WalkButton:
    position: MapPoint
    id: int


# road objects
@dataclasses.dataclass
class Lane:
    road_id: int
    lane_id: int
    type: LaneType
    polyline: List[MapPoint]
    entry_lanes: List[str]
    exit_lanes: List[str]
    boundary: List[MapPoint]

@dataclasses.dataclass
class Crosswalk:
    polygon: List[MapPoint]
    id: int

@dataclasses.dataclass
class RoadLine:
    id: int
    type: str
    polyline: List[MapPoint]


# vector map
@dataclasses.dataclass
class Map:
    map_features: List[Union[Lane, Crosswalk, RoadLine, WalkButton]]
    dynamic_states: List[DynamicState] = None


if __name__ == "__main__":
    print(Map([]))