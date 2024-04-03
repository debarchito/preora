from preora import Intersection, Road, Position
from nanoid import generate


def test(capsys):
    intr = Intersection(tag=generate(size=5))

    intr.addRoads(
        (
            (
                Road(tag=generate(size=5), avi=1, vcd=800, is_directed=True),
                Position.INCOMING_WEST,
            ),
            (
                Road(tag=generate(size=5), avi=1, vcd=800, is_directed=True),
                Position.OUTGOING_WEST,
            ),
            (
                Road(tag=generate(size=5), avi=1, vcd=700, is_directed=True),
                Position.OUTGOING_EAST,
            ),
            (
                Road(tag=generate(size=5), avi=1, vcd=700, is_directed=True),
                Position.INCOMING_EAST,
            ),
            (Road(tag=generate(size=5), avi=2, vcd=50), Position.INCOMING_NORTH),
        )
    )

    with capsys.disabled():
        print(intr.roads)
