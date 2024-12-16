import dataclasses
from typing import TypeAlias, Tuple, Sequence, Any, Generic, TypeVar, Self


Direction: TypeAlias = Tuple[int, int]


@dataclasses.dataclass
class Position:
    x: int
    y: int

    def clone(self) -> Self:
        return Position(self.x, self.y)

    def move(self, d: Direction) -> Self:
        self.x += d[0]
        self.y += d[1]
        return self

    def up(self) -> Self:
        return self.move(UP)

    def down(self) -> Self:
        return self.move(DOWN)

    def left(self) -> Self:
        return self.move(LEFT)

    def right(self) -> Self:
        return self.move(RIGHT)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def square_distance(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def direction_to_other(self, other: Self) -> Direction:
        if self.square_distance(other) > 1:
            raise ValueError('self and other must be adjacent')
        for d in [UP, DOWN, LEFT, RIGHT]:
            if self.clone().move(d) == other:
                return d
        raise AssertionError(f'other not reachable from {self} via cardinal directions')


PositionDirection: TypeAlias = Tuple[Position, Direction]


T = TypeVar("T")
class Grid(Generic[T]):
    def __init__(self, grid: Sequence[Sequence[T]]) -> None:
        self._grid = grid

    def at(self, p: Position) -> T:
        return self._grid[p.y][p.x]

    def in_bounds(self, p: Position) -> bool:
        max_x = len(self._grid[0])
        max_y = len(self._grid)
        return 0 <= p.x < max_x and 0 <= p.y < max_y


UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)
RIGHT: Direction = (1, 0)
