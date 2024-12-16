import unittest
from algorithms.grid import Grid, Position, UP, DOWN, LEFT, RIGHT


class TestPosition(unittest.TestCase):
    def test_init(self):
        p = Position(1, 2)
        assert p.x == 1
        assert p.y == 2

    def test_clone(self):
        p = Position(1, 2)
        p2 = p.clone()
        assert p == p2
        assert not p is p2

    def test_eq(self):
        p = Position(1, 2)

        p2 = p.clone()
        assert p == p2
        assert not p != p2

        p2 = p.clone().move(UP)
        assert not p == p2
        assert p != p2

    def test_move(self):
        p = Position(1, 2)
        p.move(UP)
        assert p.x == 1
        assert p.y == 1  # moved this instance

        p = Position(1, 2)
        p.clone().move(UP)
        assert p.x == 1
        assert p.y == 2  # did not move this instance

    def test_square_distance(self):
        p = Position(1, 2)
        for d in [UP, DOWN, LEFT, RIGHT]:
            p2 = p.clone().move(d)
            assert p.square_distance(p2) == 1
        p2 = Position(2, 3)
        assert p.square_distance(p2) == 2

    def test_direction_to_other(self):
        p = Position(1, 2)
        for d in [UP, DOWN, LEFT, RIGHT]:
            p2 = p.clone().move(d)
            assert p.direction_to_other(p2) == d
        p2 = Position(2, 3)
        self.assertRaises(ValueError, p.direction_to_other, p2)


class TestGrid(unittest.TestCase):
    def setUp(self):
        g1 = [  # List of strings
            '1234',
            '5678',
            'abcd',
        ]
        g2 = [[x for x in e] for e in g1]  # List of lists
        self.grid1 = Grid(g1)
        self.grid2 = Grid(g2)

    def test_grid(self):
        for grid in [self.grid1, self.grid2]:
            assert grid.at(Position(0, 0)) == '1'
            assert grid.at(Position(0, 1)) == '5'
            assert grid.at(Position(1, 1)) == '6'
            self.assertRaises(IndexError, grid.at, Position(0, 4))

    def test_at(self):
        for grid in [self.grid1, self.grid2]:
            assert grid.in_bounds(Position(0, 0)) == True
            assert grid.in_bounds(Position(0, 1)) == True
            assert grid.in_bounds(Position(-1, 1)) == False
            assert grid.in_bounds(Position(-1, -1)) == False
            assert grid.in_bounds(Position(1, -1)) == False
            assert grid.in_bounds(Position(1, 4)) == False
