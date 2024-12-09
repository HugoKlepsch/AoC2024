import itertools
import timeit
import typing
import dataclasses


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def p1():
    all_antennas, max_xy = read_parse()
    antinodes: typing.Dict[Point, str] = {}
    for frequency, antennas in all_antennas.items():
        for pair in itertools.permutations(antennas, 2):
            assert pair[0] != pair[1]
            antinode = half_antinode(pair[0], pair[1])
            if in_bounds(antinode, max_xy):
                if antinode not in antinodes:
                    antinodes[antinode] = frequency

    score = len(antinodes)
    print(score)


def p2():
    all_antennas, max_xy = read_parse()
    antinodes: typing.Dict[Point, str] = {}
    for frequency, antennas in all_antennas.items():
        if len(antennas) >= 3:
            for antenna in antennas:
                antinodes[antenna] = frequency
        for pair in itertools.permutations(antennas, 2):
            a = pair[0]
            b = pair[1]
            antinode = half_antinode(a, b)
            while in_bounds(antinode, max_xy):
                antinodes[antinode] = frequency
                a = b
                b = antinode
                antinode = half_antinode(a, b)

    score = len(antinodes)

    print(score)


def half_antinode(a: Point, b: Point) -> Point:
    dx, dy = b.x - a.x, b.y - a.y
    return Point(b.x + dx, b.y + dy)


def in_bounds(p: Point, max_inclusive: Point, min_inclusive: Point=Point(0, 0)) -> bool:
    return min_inclusive.x <= p.x <= max_inclusive.x and min_inclusive.y <= p.y <= max_inclusive.y


def print_all(max_xy: Point, antennas: typing.Dict[str, typing.List[Point]], antinodes: typing.Dict[Point, str]) -> None:
    '''
    max_xy = (2,3)
         012
        0...
        1...
        2...
        3...
    '''
    output = ''
    for y in range(max_xy.y + 1):
        for x in range(max_xy.x + 1):
            p = Point(x, y)
            # check for antennas
            found = False
            for c, l in antennas.items():
                if p in l:
                    output += c
                    found = True
                    break
            if found:
                continue

            # check for antinodes
            found = False
            for point, c in antinodes.items():
                if p == point:
                    output += '#'
                    found = True
                    break
            if found:
                continue
            output += '.'
        output += '\n'
    print(output)


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    antennas: typing.Dict[str, typing.List[Point]] = {}
    x, y = 0, 0
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c != '.':
                l = antennas.get(c, [])
                l.append(Point(x, y))
                antennas[c] = l
    return antennas, Point(x, y)


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
