"""
Preora: A framework to build and optimize traffic intersections.
"""

import polars as pl


class Road:
    def __init__(self, *, tag: str, avi: int, vcd: int, is_directed=False):
        self.df = pl.DataFrame(
            {
                "tag": tag,
                "avi": avi,
                "vcd": vcd,
                "is_directed": is_directed,
            }
        )

    @staticmethod
    def from_df(*, df: pl.DataFrame):
        """
        Creates a `Road` object from a `Polars DataFrame`.
        """
        road = Road(
            tag=df["tag"], avi=df["avi"], vcd=df["vcd"], is_directed=df["is_directed"]
        )
        return road


class Intersection:
    def __init__(self, *, tag: str):
        self.tag = tag
        self.roads = []

    def addRoad(self, *, road: Road):
        self.roads.append(road)

    def addRoads(self, *, roads: list[Road]):
        self.roads.extend(roads)
