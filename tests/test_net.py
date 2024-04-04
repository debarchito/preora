import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from preora import Position

G = nx.DiGraph()
G.add_node("Intersection")

roads = [
    ("R1", 1, 800, True, Position.INCOMING_WEST),
    ("R2", 1, 800, True, Position.OUTGOING_WEST),
    ("R3", 1, 700, True, Position.OUTGOING_EAST),
    ("R4", 1, 700, True, Position.INCOMING_EAST),
    ("R5", 2, 50, False, Position.INCOMING_NORTH),
]

for road_data in roads:
    road_tag, avi, vcd, is_directed, position = road_data

    if not is_directed:
        G.add_node(road_tag, "Intersection", position=position.value, arrowstyle="-")
        continue

    if position.value < np.pi * 2:
        G.add_edge(road_tag, "Intersection", position=position.value, arrowstyle="->")
    else:
        G.add_edge("Intersection", road_tag, position=position.value, arrowstyle="->")

fixed_positions = {
    "Intersection": (0, 0),
    "R1": (np.sin(Position.INCOMING_WEST + 0.1), np.cos(Position.INCOMING_WEST + 0.1)),
    "R3": (np.sin(Position.OUTGOING_WEST), np.cos(Position.OUTGOING_WEST)),
    "R2": (np.sin(Position.OUTGOING_EAST), np.cos(Position.OUTGOING_EAST)),
    "R4": (np.sin(Position.INCOMING_EAST + 0.1), np.cos(Position.INCOMING_EAST + 0.1)),
    "R5": (np.sin(Position.INCOMING_NORTH), np.cos(Position.INCOMING_NORTH)),
}

fixed_nodes = fixed_positions.keys()
pos = fixed_positions

fig, ax = plt.subplots()

nx.draw_networkx_nodes(
    G, pos, nodelist=fixed_nodes, node_size=700, node_color="r", ax=ax
)

edges = G.edges(data=True)
edge_arrows = {}
for u, v, data in edges:
    position = data["position"]
    if position < np.pi * 2:
        edge_color = "b"
    else:
        edge_color = "r" if data["arrowstyle"] == "->" else "g"
    edge_collection = nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(u, v)],
        edge_color=edge_color,
        arrows=False,
        width=2,
        ax=ax,
    )
    edge_arrows[edge_collection] = (u, v)

nx.draw_networkx_labels(G, pos, ax=ax)

circle = plt.Circle((0, 0), radius=1, color="b", fill=False, linestyle="dotted")
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


ani = FuncAnimation(fig, update, frames=np.arange(0, 101), interval=0)
plt.title("Road Connections")
plt.axis("off")
plt.show()
