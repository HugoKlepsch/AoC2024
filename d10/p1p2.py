import timeit
import typing


def p1():
    grid = read_parse()
    starts = get_starts(grid)

    score = 0
    for start in starts:
        exits_seen: typing.Set[typing.Tuple[int, int]] = set()
        to_check: typing.List[typing.Tuple[int, int]] = [start]
        for tup in to_check:
            cur_e = get_e(grid, tup)
            if cur_e == 9:
                if tup not in exits_seen:
                    exits_seen.add(tup)
                    score += 1
            to_check.extend(get_passable(grid, tup))
    print(score)


def p2():
    grid = read_parse()
    starts = get_starts(grid)

    score = 0
    for start in starts:
        to_check: typing.List[typing.Tuple[int, int]] = [start]
        for tup in to_check:
            cur_e = get_e(grid, tup)
            if cur_e == 9:
                score += 1
            to_check.extend(get_passable(grid, tup))
    print(score)


def get_starts(grid: typing.List[typing.List[int]]) -> typing.Set[typing.Tuple[int, int]]:
    starts: typing.Set[typing.Tuple[int, int]] = set()
    for y, line in enumerate(grid):
        for x, e in enumerate(line):
            if e == 0:
                tup = (x, y)
                starts.add(tup)
    return starts


def up(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0], coord[1] - 1


def down(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0], coord[1] + 1


def left(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0] - 1, coord[1]


def right(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0] + 1, coord[1]


def in_bounds(grid: typing.List[typing.List[int]], at: typing.Tuple[int, int]) -> bool:
    return 0 <= at[1] < len(grid) and 0 <= at[0] < len(grid[0])


def get_e(grid: typing.List[typing.List[int]], at: typing.Tuple[int, int]) -> int:
    return grid[at[1]][at[0]]


def get_passable(grid: typing.List[typing.List[int]], at: typing.Tuple[int, int]) -> typing.Set[typing.Tuple[int, int]]:
    passable: typing.Set[typing.Tuple[int, int]] = set()
    cur_e = get_e(grid, at)
    # check up
    other_tup = up(at)
    if in_bounds(grid, other_tup):
        other_e = get_e(grid, other_tup)
        if other_e == cur_e + 1:
            passable.add(other_tup)
    # check down
    other_tup = down(at)
    if in_bounds(grid, other_tup):
        other_e = get_e(grid, other_tup)
        if other_e == cur_e + 1:
            passable.add(other_tup)
    # check left
    other_tup = left(at)
    if in_bounds(grid, other_tup):
        other_e = get_e(grid, other_tup)
        if other_e == cur_e + 1:
            passable.add(other_tup)
    # check right
    other_tup = right(at)
    if in_bounds(grid, other_tup):
        other_e = get_e(grid, other_tup)
        if other_e == cur_e + 1:
            passable.add(other_tup)
    return passable



def read_parse():
    with open('input') as f:
        lines = f.readlines()
    grid: typing.List[typing.List[int]] = []
    for line in lines:
        grid_line = []
        for c in line.strip():
            try:
                num = int(c)
            except ValueError:
                num = -9999
            grid_line.append(num)
        grid.append(grid_line)
    return grid


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
