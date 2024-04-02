from preora import Intersection, Road


def test(capsys):
    intr = Intersection(tag="A")
    road_one = Road(tag="R1", avi=1, vcd=1200, is_directed=False)
    intr.addRoad(road=road_one)

    with capsys.disabled():
        print(intr.roads)
