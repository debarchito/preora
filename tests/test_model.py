from preora import Intersection, Road, Position, GenericPosition
from nanoid import generate
import numpy as np


def test(capsys):
    intr = Intersection(tag=generate(size=5))

    intr.addRoads(
        (
            (
                Road(tag="R1", avi=1, vcd=800, is_directed=True),
                GenericPosition(Position.WEST + 0.05),
            ),
            (
                Road(tag="R2", avi=1, vcd=800, is_directed=True),
                Position.OUTGOING_WEST,
            ),
            (
                Road(tag="R3", avi=1, vcd=700, is_directed=True),
                Position.OUTGOING_EAST,
            ),
            (
                Road(tag="R4", avi=1, vcd=700, is_directed=True),
                GenericPosition(Position.EAST + 0.05),
            ),
            (Road(tag="R5", avi=2, vcd=50), GenericPosition(np.pi / 4)),
        )
    )

    intr.plot()

    with capsys.disabled():
        print(intr.roads)
