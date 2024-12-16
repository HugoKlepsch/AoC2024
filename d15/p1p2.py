import timeit
import typing


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def p1():
    grid, moves = read_parse()
    rp = (0, 0)
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == '@':
                rp = x, y
    for move_t in moves:
        move = move_t[0]
        result = push(grid, rp, move, do_swap=True)
        if result:
            rp = point_and_dir(rp, move)
    score = 0
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == 'O':
                score += 100 * y + x
    print(score)


def p2():
    grid, moves = read_parse()
    # expand grid
    new_grid = []
    for y, line in enumerate(grid):
        new_grid_line = []
        for x, v in enumerate(line):
            if v == '@':
                new_grid_line.append('@')
                new_grid_line.append('.')
            elif v == '.':
                new_grid_line.append('.')
                new_grid_line.append('.')
            elif v == '#':
                new_grid_line.append('#')
                new_grid_line.append('#')
            elif v == 'O':
                new_grid_line.append('[')
                new_grid_line.append(']')
        new_grid.append(new_grid_line)
    grid = new_grid
    del new_grid
    rp = (0, 0)
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == '@':
                rp = x, y
    print_grid(grid)
    for move_t in moves:
        move = move_t[0]
        move_c = move_t[1]
        result = push(grid, rp, move, do_swap=False)
        if result:
            _ = push(grid, rp, move, do_swap=True)
            rp = point_and_dir(rp, move)
        print(f'-----')
        print(f'After applying {move_c}')
        print_grid(grid)
    score = 0
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == '[':
                score += 100 * y + x
    print(score)


def print_grid(grid):
    output = ''
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            output += v
        output += '\n'
    print(output)


def swap_ps(grid, pa, pb):
    c = at(grid, pa)
    set_at(grid, pa, at(grid, pb))
    set_at(grid, pb, c)


def push(grid, from_p: typing.Tuple[int, int], dir: typing.Tuple[int, int], do_swap=False) -> bool:
    dst = point_and_dir(from_p, dir)
    dst_c = at(grid, dst)
    if dst_c == '.':
        if do_swap:
            swap_ps(grid, from_p, dst)
        return True
    elif dst_c == '#':
        return False
    elif dst_c == 'O':
        next_move = push(grid, dst, dir, do_swap)
        if next_move:
            if do_swap:
                swap_ps(grid, from_p, dst)
        return next_move
    elif dst_c == '[':
        if dir in {UP, DOWN}:
            to_check = [(dst, dir), (right(dst), dir)]
        else:
            to_check = [(dst, dir)]
        next_move = all((push(grid, check[0], check[1], do_swap) for check in to_check))
        if do_swap:
            swap_ps(grid, from_p, dst)
        return next_move
    elif dst_c == ']':
        if dir in {UP, DOWN}:
            to_check = [(dst, dir), (left(dst), dir)]
        else:
            to_check = [(dst, dir)]
        next_move = all((push(grid, check[0], check[1], do_swap) for check in to_check))
        if do_swap:
            swap_ps(grid, from_p, dst)
        return next_move
    raise AssertionError(f'This should never happen. from_p = {from_p}, dir = {dir}, dst_c = {dst_c}')


def at(grid, p):
    return grid[p[1]][p[0]]


def set_at(grid, p, c):
    grid[p[1]][p[0]] = c


def point_and_dir(p, dir):
    x, y = p
    dx, dy = dir
    return x + dx, y + dy


def up(p):
    return point_and_dir(p, UP)


def down(p):
    return point_and_dir(p, DOWN)


def left(p):
    return point_and_dir(p, LEFT)


def right(p):
    return point_and_dir(p, RIGHT)


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    grid = []
    moves = []

    parsing_moves = False
    for line in lines:
        if line == '\n':
            parsing_moves = True
            continue

        if not parsing_moves:
            grid.append([c for c in line.strip()])
        else:
            for c in line.strip():
                if c == '^':
                    moves.append((UP, c))
                elif c == 'v':
                    moves.append((DOWN, c))
                elif c == '<':
                    moves.append((LEFT, c))
                elif c == '>':
                    moves.append((RIGHT, c))
    return grid, moves


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
