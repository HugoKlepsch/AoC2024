'''
This isn't the cleanest code, but it works
'''
import timeit
import typing


def p1():
    grid = read_parse()

    score = 0
    processed_tups: typing.Set[typing.Tuple[int, int]] = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            tup = (x, y)
            if tup not in processed_tups:
                area, fence_perimeter, _ = area_fence_perimeter(grid, tup, processed_tups)
                score += fence_perimeter * area
                region = grid[tup[1]][tup[0]]

    print(score)


def p2():
    grid = read_parse()

    score = 0
    processed_coords: typing.Set[typing.Tuple[int, int]] = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            coord = (x, y)
            if coord not in processed_coords:
                region = grid[coord[1]][coord[0]]
                area, _, perimeter = area_fence_perimeter(grid, coord, processed_coords)
                num_sides = sides(perimeter)
                score += area * num_sides

    print(score)


def up(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0], coord[1] - 1


def down(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0], coord[1] + 1


def left(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0] - 1, coord[1]


def right(coord: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return coord[0] + 1, coord[1]


def area_fence_perimeter(
        grid: typing.List[str],
        tup: typing.Tuple[int, int],
        all_seen: typing.Set[typing.Tuple[int, int]]
) -> typing.Tuple[int, int, typing.Set[typing.Tuple[typing.Tuple[int, int], int]]]:
    seen = set()
    to_visit: typing.List[typing.Tuple[int, int]] = [tup]
    region = grid[tup[1]][tup[0]]
    area = 0
    fence_perimiter_count = 0
    fence_perimeter: typing.Set[typing.Tuple[typing.Tuple[int, int], int]] = set()
    for tup in to_visit:
        if tup in seen or tup in all_seen:
            continue
        seen.add(tup)
        all_seen.add(tup)
        area += 1

        for other_tup_fn in [(up, UP), (down, DOWN), (left, LEFT), (right, RIGHT)]:
            other_tup = other_tup_fn[0](tup)
            other_region = None
            if in_bounds(grid, other_tup):
                other_region = grid[other_tup[1]][other_tup[0]]
            if other_region == region:
                to_visit.append(other_tup)
            else:
                fence_perimiter_count += 1
                fence_perimeter.add((other_tup, other_tup_fn[1]))

    return area, fence_perimiter_count, fence_perimeter


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


def sides(
        perimeter: typing.Set[typing.Tuple[typing.Tuple[int, int], int]],
) -> int:
    '''
    AA
    AB

    Given the above shape, the perimeter of each contiguous region should include:
    A
    - ((0, 0), UP)
    - ((0, 0), LEFT)
    - ((1, 0), UP)
    - ((1, 0), RIGHT)
    - ((1, 0), DOWN)
    - ((0, 1), RIGHT)
    - ((0, 1), DOWN)
    - ((0, 1), LEFT)
    B
    - ((1, 1), UP)
    - ((1, 1), RIGHT)
    - ((1, 1), DOWN)
    - ((1, 1), LEFT)

    Pass the parameter of just one contiguous region. sides will return the number of contiguous sides
    of that shape. For A, it is 6. For B it is 4.
    '''
    seen: typing.Set[typing.Tuple[typing.Tuple[int, int], int]] = set()
    side_count = 0
    for fence in perimeter:
        if fence in seen:
            continue
        seen.add(fence)
        side_count += 1
        side_seen: typing.Set[typing.Tuple[typing.Tuple[int, int], int]] = set(fence)
        to_visit: typing.List[typing.Tuple[typing.Tuple[int, int], int]] = [fence]
        for fence in to_visit:
            seen.add(fence)
            fence_direction = fence[1]
            if fence_direction in [UP, DOWN]:
                search_directions = [left, right]
            elif fence_direction in [LEFT, RIGHT]:
                search_directions = [up, down]
            else:
                raise ValueError(f'Unknown perimeter direction: {fence_direction}')
            for dir_fn in search_directions:
                other_tup = (dir_fn(fence[0]), fence_direction)
                if other_tup in perimeter and other_tup not in side_seen:
                    side_seen.add(other_tup)
                    to_visit.append(other_tup)
    return side_count


def in_bounds(grid: typing.List[str], tup: typing.Tuple[int, int]) -> bool:
    return 0 <= tup[1] < len(grid) and 0 <= tup[0] < len(grid[0])


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    return [
        line.strip()
        for line in lines
    ]


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
