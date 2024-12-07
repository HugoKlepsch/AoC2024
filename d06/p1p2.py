import dataclasses
import typing
from copy import deepcopy

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

GUARD_START = '^'
VISITED = 'X'
OBSTACLE = '#'

GridSquare: type = str


@dataclasses.dataclass
class Guard:
    coord: typing.Tuple[int, int]
    direction: typing.Tuple[int, int]

def p1():
    grid = read_parse()

    guard = find_guard(grid)

    guard_present = True
    while guard_present:
        guard_left, _ = iterate(grid, guard)
        guard_present = not guard_left

    # find how many grids were visited
    score = 0
    for y, line in enumerate(grid):
        for x, gridSquare in enumerate(line):
            if gridSquare == VISITED:
                score += 1

    print(score)


def p2():
    # The strategy is to brute force the solution, but in a hopefully slightly more efficient way:
    # The pure brute force solution is to place an obstacle in each grid square, then run the simulation looking for
    # loops. The way I want to try is to only try placing an obstacle in grids surrounding those that are possible to
    # hit; grid squares in front of where the guard goes.
    grid_start = read_parse()
    grid = deepcopy(grid_start)

    guard_start = find_guard(grid)
    guard: Guard = deepcopy(guard_start)

    possible_loop_obstacles: typing.Set[typing.Tuple[int, int]] = set()
    guard_present = True
    while guard_present:
        where_guard_could_go = (guard.coord[0] + guard.direction[0], guard.coord[1] + guard.direction[1])
        if where_guard_could_go[0] < 0 or where_guard_could_go[0] >= len(grid[0]) or where_guard_could_go[1] < 0 or where_guard_could_go[1] >= len(grid):
            # Out of bounds; do nothing
            pass
        else:
            possible_loop_obstacles.add(where_guard_could_go)
        guard_left, _ = iterate(grid, guard)
        possible_loop_obstacles.add(guard.coord)
        guard_present = not guard_left

    print(f'Need to check {len(possible_loop_obstacles)} obstacles for loops.')
    # find how many of these could create a loop
    score = 0
    for obstacle_i, obstacle in enumerate(possible_loop_obstacles):
        print(f'Checking {obstacle_i}: {obstacle}')
        visited = set()
        grid = deepcopy(grid_start)
        guard = deepcopy(guard_start)
        grid[obstacle[1]][obstacle[0]] = OBSTACLE
        while True:
            guard_left, loop_detected = iterate(grid, guard, visited)
            if loop_detected:
                score += 1
                break
            if guard_left:
                break

    print(score)


def find_guard(grid: typing.List[typing.List[GridSquare]]) -> Guard:
    guard = None
    for y, line in enumerate(grid):
        for x, gridSquare in enumerate(line):
            if gridSquare == GUARD_START:
                guard = Guard((x, y), UP)
    assert guard
    return guard


# iterate returns:
# - whether the guard left the grid
# - whether the guard entered a square in the same direction as previously
def iterate(
        grid: typing.List[typing.List[GridSquare]],
        guard: Guard,
        visited: typing.Set[typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]]=None
) -> typing.Tuple[bool, bool]:
    if visited is not None:
        coord_dir = (guard.coord, guard.direction)
        if coord_dir in visited:
            # Entered the same grid as before, in the same direction as before; we will loop.
            return False, True
        visited.add(coord_dir)
    next_coord = (guard.coord[0] + guard.direction[0], guard.coord[1] + guard.direction[1])

    # if the next coordinate is out of bounds, the guard leaves
    if next_coord[0] < 0 or next_coord[0] >= len(grid[0]) or next_coord[1] < 0 or next_coord[1] >= len(grid):
        grid[guard.coord[1]][guard.coord[0]] = VISITED
        return True, False

    next_grid = grid[next_coord[1]][next_coord[0]]
    if next_grid == OBSTACLE:
        # guard turns 90 degrees
        if guard.direction == UP:
            guard.direction = RIGHT
        elif guard.direction == RIGHT:
            guard.direction = DOWN
        elif guard.direction == DOWN:
            guard.direction = LEFT
        elif guard.direction == LEFT:
            guard.direction = UP
    else:
        # guard can move
        grid[guard.coord[1]][guard.coord[0]] = VISITED
        guard.coord = next_coord
    return False, False


def print_grid(grid: typing.List[typing.List[GridSquare]]):
    output = ''
    for y, line in enumerate(grid):
        for x, gridSquare in enumerate(line):
            output += gridSquare
        output += '\n'
    print(output)


def read_parse():
    grid: typing.List[typing.List[GridSquare]] = []
    with open('input') as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            if line == '\n':
                continue
            grid.append([])
            for x, char in enumerate(line):
                if char == '\n':
                    continue
                grid[y].append(char)
    return grid


if __name__ == '__main__':
    p1()
    p2()