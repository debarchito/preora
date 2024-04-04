"""
Preora: A framework to build and optimize traffic intersections.
"""

from enum import Enum
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


class Position(float, Enum):
    INCOMING_NORTH = 0
    NORTH = 0  # Alias for INCOMING_NORTH
    INCOMING_EAST = np.pi / 2
    EAST = np.pi / 2  # Alias for INCOMING_EAST
    INCOMING_SOUTH = np.pi
    SOUTH = np.pi  # Alias for INCOMING_SOUTH
    INCOMING_WEST = 3 * np.pi / 2
    WEST = 3 * np.pi / 2  # Alias for INCOMING_WEST
    OUTGOING_NORTH = 2 * np.pi
    OUTGOING_EAST = 5 * np.pi / 2
    OUTGOING_SOUTH = 3 * np.pi
    OUTGOING_WEST = 7 * np.pi / 2


class GenericPosition:
    def __init__(self, value: int):
        self.name = "GENERIC"
        self.value = value


class Road:
    def __init__(self, tag: str, avi: int, vcd: int, is_directed=False):
        self.details = {"tag": tag, "avi": avi, "vcd": vcd, "is_directed": is_directed}

    def copy_with_new_tag(self, tag: str):
        return Road(
            tag=tag,
            avi=self.details["avi"],
            vcd=self.details["vcd"],
            is_directed=self.details["is_directed"],
        )


class Crossing:
    def __init__(self, tag: str, from_: str, to: str, pcd: int):
        self.details = {"tag": tag, "from": from_, "to": to, "pcd": pcd}


class Entity:
    def __init__(self, tag: str, avi: int):
        self.details = {"tag": tag, "avi": avi}

    def copy_with_new_tag(self, tag: str):
        return Entity(tag=tag, avi=self.details["avi"])


class Intersection:
    def __init__(self, tag: str):
        self.tag = tag
        self.roads = pl.DataFrame(
            schema={
                "tag": pl.Utf8(),  # Unique identifier for the road
                "avi": pl.Int64(),  # Allowable Vehicle Index
                "vcd": pl.Int64(),  # Vehicle Crowding Density
                "is_directed": pl.Boolean(),  # Is the road one-way?
                "position": pl.Float64(),  # Position of the road in radians
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
        road.details["position"] = dir.value if dir else 0.0
        self.roads = pl.concat([self.roads, pl.DataFrame(road.details)]).unique(
            subset=["tag"], keep="last"
        )

    def addCrossing(self, crossing: Crossing):
        self.crossings = pl.concat(
            [self.crossings, pl.DataFrame(crossing.details)]
        ).unique(subset=["tag"], keep="last")

    def addEntity(self, entity: Entity):
        self.entities = pl.concat([self.entities, pl.DataFrame(entity.details)]).unique(
            subset=["tag"], keep="last"
        )

    def addRoads(self, roads: tuple[tuple[Road, Position | GenericPosition | None]]):
        for road, dir in roads:
            self.addRoad(road, dir)

    def addCrossings(self, crossings: tuple[Crossing]):
        for crossing in crossings:
            self.addCrossing(crossing)

    def addEntities(self, entities: tuple[Entity]):
        for entity in entities:
            self.addEntity(entity)

    def visualize_model(self):
        G = nx.DiGraph()
        G.add_node(self.tag)

        for _, row in self.roads.to_pandas().iterrows():
            if row["position"] < np.pi * 2:
                if row["is_directed"]:
                    G.add_edge(
                        row["tag"],
                        self.tag,
                        position=row["position"],
                        arrowstyle="->",
                        linestyle="solid",
                    )
                else:
                    G.add_edge(
                        row["tag"],
                        self.tag,
                        position=row["position"],
                        arrowstyle="-",
                        linestyle="-.",
                    )
            else:
                if row["is_directed"]:
                    G.add_edge(
                        self.tag,
                        row["tag"],
                        position=row["position"],
                        arrowstyle="->",
                        linestyle="solid",
                    )
                else:
                    G.add_edge(
                        self.tag,
                        row["tag"],
                        position=row["position"],
                        arrowstyle="-",
                        linestyle="-.",
                    )

        fixed_positions = {
            self.tag: (0, 0),
        }

        for i, row in self.roads.to_pandas().iterrows():
            if row["tag"] != self.tag:
                fixed_positions[row["tag"]] = (
                    np.sin(row["position"] + 0.1),
                    np.cos(row["position"] + 0.1),
                )

        fixed_nodes = fixed_positions.keys()
        pos = fixed_positions

        fig, ax = plt.subplots()

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=fixed_nodes,
            node_size=700,
            node_color="#dad8e8",
            node_shape="h",
            ax=ax,
        )

        edges = G.edges(data=True)
        edge_arrows = {}
        for u, v, data in edges:
            position = data["position"]
            if position < np.pi * 2:
                edge_color = "#6787bc"
            else:
                edge_color = "#e29b72" if data["arrowstyle"] == "->" else "#95c9a1"
            edge_collection = nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[(u, v)],
                edge_color=edge_color,
                style=data["linestyle"],
                arrows=False,
                width=3,
                ax=ax,
            )
            edge_arrows[edge_collection] = (u, v)

        nx.draw_networkx_labels(G, pos, ax=ax)

        circle = plt.Circle(
            (0, 0), radius=1, color="#8172b3", fill=False, linestyle="dotted"
        )
        ax.add_patch(circle)

        def update(frame):
            for edge_collection, (u, v) in edge_arrows.items():
                if G[u][v]["arrowstyle"] == "->":
                    x0, y0 = pos[u]
                    x1, y1 = pos[v]
                    dx = (x1 - x0) * (frame / 100)
                    dy = (y1 - y0) * (frame / 100)
                    new_positions = np.array([[x0 + dx, y0 + dy], [x0, y0]])
                    edge_collection.set_segments([new_positions])

        road_tags = self.roads["tag"].to_numpy()
        road_avis = self.roads["avi"].to_numpy()
        road_vcd = self.roads["vcd"].to_numpy()

        legend_labels = [
            f"{tag} (AVI: {avi}, VCD: {vcd})"
            for tag, avi, vcd in zip(road_tags, road_avis, road_vcd)
        ]
        plt.legend(
            legend_labels,
            loc="upper right",
            title="Roads",
            fontsize="medium",
            frameon=True,
            handlelength=0,
            handleheight=0,
        )
        # plt.setp(legend.get_title(), fontsize="medium")

        _ = FuncAnimation(fig, update, frames=np.arange(0, 101), interval=0)
        plt.title("Road Connections")
        plt.axis("off")
        plt.show()
