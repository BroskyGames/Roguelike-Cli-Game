from game.core.geometry import Pos, Size, Vector2


def test_size_uniqueness():
    seen = set()
    for x in range(1, 33):
        for y in range(1, 33):
            p = Size(x, y).__hash__()
            assert p not in seen
            seen.add(p)


def test_pos_uniqueness():
    seen = set()
    for x in range(-511, 512):
        for y in range(-511, 512):
            p = Pos(x, y).__hash__()
            assert p not in seen
            seen.add(p)


def test_vector_uniqueness():
    seen = set()
    for x in range(-511, 512):
        for y in range(-511, 512):
            p = Vector2(x, y).__hash__()
            assert p not in seen
            seen.add(p)


def test_pos_vector_arithmetics():
    assert Pos(3, 5) - Pos(7, 5) == Vector2(-4, 0)
    assert Pos(3, 5) + Vector2(-4, 3) == Pos(-1, 8)
    assert Pos(3, 5) + -Vector2(4, -3) == Pos(-1, 8)
    assert Pos(3, 5) + -Vector2(4, -3) == Pos(-1, 8)
    assert Vector2(3, 5) + -Vector2(4, -3) == Vector2(-1, 8)
