from preora import Intersection, Road, Position, GenericPosition
from nanoid import generate


def test(capsys):
    intr = Intersection(tag=generate(size=5))

    road_one = Road(tag=generate(size=5), avi=1, vcd=1200)
    road_two = road_one.copy_with_new_tag(tag=generate(size=5))
    road_three = road_two.copy_with_new_tag(tag=generate(size=5))
    road_four = Road(tag=generate(size=5), avi=2, vcd=50, is_directed=True)

    intr.addRoads(
        [
            (road_one, Position.NORTH),
            (road_two, GenericPosition(272)),
            (road_three, None),
            (road_four, Position.SOUTH),
            (road_four, Position.WEST),
        ]
    )

    with capsys.disabled():
        print(intr.roads)
