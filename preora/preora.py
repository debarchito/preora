"""
Preora: A framework to build and optimize traffic intersections.
"""

from enum import Enum
import polars as pl


class Position(Enum):
    INCOMING_NORTH = 0
    NORTH = 0  # Alias for INCOMING_NORTH
    INCOMING_EAST = 90
    EAST = 90  # Alias for INCOMING_EAST
    INCOMING_SOUTH = 180
    SOUTH = 180  # Alias for INCOMING_SOUTH
    INCOMING_WEST = 270
    WEST = 270  # Alias for INCOMING_WEST
    OUTGOING_NORTH = 360
    OUTGOING_EAST = 450
    OUTGOING_SOUTH = 540
    OUTGOING_WEST = 630


class GenericPosition:
    def __init__(self, value: int):
        self.name = "GENERIC"
        self.value = value


class Road:
    def __init__(self, *, tag: str, avi: int, vcd: int, is_directed=False):
        self.details = {"tag": tag, "avi": avi, "vcd": vcd, "is_directed": is_directed}

    def copy_with_new_tag(self, *, tag: str):
        return Road(
            tag=tag,
            avi=self.details["avi"],
            vcd=self.details["vcd"],
            is_directed=self.details["is_directed"],
        )


class Intersection:
    def __init__(self, *, tag: str):
        self.tag = tag
        self.roads = pl.DataFrame(
            schema={
                "tag": pl.Utf8(),  # Unique identifier for the road
                "avi": pl.Int64(),  # Allowable Vehicle Index
                "vcd": pl.Int64(),  # Vehicle Crowding Density
                "is_directed": pl.Boolean(),  # Is the road one-way?
                "position": pl.Int64(),  # Direction of the road in degrees
            }
        )
        self.entities = pl.DataFrame(
            schema={
                "tag": pl.Utf8(),  # Unique identifier for the entity
                "avi": pl.Int64(),  # Allowable Vehicle Index
            }
        )
        self.crossings = pl.DataFrame(
            schema={
                "tag": pl.Utf8(),  # Unique identifier for the crossing
                "from": pl.Utf8(),  # Road from which the crossing originates
                "to": pl.Utf8(),  # Road to which the crossing leads
                "pcd": pl.Int64(),  # Pedestrian Crowding Density
            }
        )

    def addRoad(self, road: Road, dir: Position | GenericPosition | None = None):
        road.details["position"] = dir.value if dir else 0
        self.roads = pl.concat([self.roads, pl.DataFrame(road.details)]).unique(
            subset=["tag"],
        )

    def addRoads(self, roads: tuple[tuple[Road, Position | GenericPosition | None]]):
        for road, dir in roads:
            self.addRoad(road, dir)
