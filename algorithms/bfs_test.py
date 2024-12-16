import unittest
from typing import List

from algorithms.bfs import BFSState, bfs
from algorithms.grid import Position, Grid, UP, DOWN, LEFT, RIGHT


class TestBFSState(unittest.TestCase):
    def setUp(self):
        self.p = Position(1, 2)
        self.my_data = {'foo': 'bar'}

    def test_init(self):
        s = BFSState(self.p, self.my_data)
        assert s.p == self.p
        assert s.data == self.my_data

    def test_clone(self):
        s = BFSState(self.p, self.my_data)
        s2 = s.clone()
        assert s == s2
        assert s is not s2
        assert s.p == s2.p
        assert s.p is not s2.p
        assert s.data == s2.data
        assert s.data is not s2.data

    def test_clone_keep_data(self):
        s = BFSState(self.p, self.my_data)
        s2 = s.clone_keep_data()
        assert s == s2
        assert s is not s2
        assert s.p == s2.p
        assert s.p is not s2.p
        assert s.data == s2.data
        assert s.data is s2.data

class TestBFS(unittest.TestCase):
    def setUp(self):
        g = [
            '######',
            '#....#',
            '#..#.#',
            '#.#..#',
            '######',
        ]
        self.num_visitable = sum((line.count('.') for line in g))
        self.grid = Grid(g)

    def test_bfs(self):
        visited_count = 0
        def visit(grid: Grid, s: BFSState):
            nonlocal visited_count
            if grid.at(s.p) == '#':
                raise AssertionError(f'Should not have visited {s.p}')
            visited_count += 1

        def next_ps(grid: Grid, s: BFSState) -> List[BFSState]:
            to_visit: List[BFSState] = []
            for d in [UP, DOWN, LEFT, RIGHT]:
                dst = s.p.clone().move(d)
                if grid.in_bounds(dst):
                    dst_c = grid.at(dst)
                    if dst_c != '#':
                        to_visit.append(BFSState(dst))
            return to_visit

        bfs(self.grid, BFSState(Position(1, 1)), visit, next_ps)
        assert visited_count == self.num_visitable