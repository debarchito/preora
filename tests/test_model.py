from preora import Intersection, Road, Position, GenericPosition


def test(capsys):
    intr = Intersection(tag="I1")

    intr.addRoads(
        (
            (
                Road(tag="R1", avi=1, vcd=200),
                Position.WEST,
            ),
            (
                Road(tag="R2", avi=2, vcd=80),
                GenericPosition(Position.INCOMING_NORTH + 0.23),
            ),
            (
                Road(tag="R3", avi=1, vcd=800, is_directed=True),
                GenericPosition(Position.OUTGOING_WEST + 0.15),
            ),
            (
                Road(tag="R4", avi=1, vcd=500, is_directed=True),
                GenericPosition(Position.OUTGOING_EAST - 0.4),
            ),
            (
                Road(tag="R5", avi=1, vcd=600, is_directed=False),
                GenericPosition(Position.OUTGOING_EAST + 0.4),
            ),
        )
    )

    intr.visualize_model()

    with capsys.disabled():
        print(intr.roads)
