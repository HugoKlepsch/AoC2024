import functools
import math
import timeit
import typing


def p1():
    rocks = read_parse()
    steps = 25

    score = 0
    for rock in rocks:
        score += count_eval_rock(rock, steps)

    print(score)


def p2():
    rocks = read_parse()
    steps = 75

    score = 0
    for rock in rocks:
        score += count_eval_rock(rock, steps)

    print(score)


@functools.cache
def count_eval_rock(rock: int, steps: int) -> int:
    if steps == 0:
        return 1
    eval_results = eval_rock(rock)
    recursive_count = 0
    for rock in eval_results:
        recursive_count += count_eval_rock(rock, steps - 1)
    return recursive_count


def eval_rock(rock: int) -> typing.List[int]:
    if rock == 0:
        eval_result = [1]
    else:
        num_digits = math.ceil(math.log10(rock + 1))
        if num_digits % 2 == 0:
            factor = (10 ** (num_digits // 2))
            first_half = rock // factor
            second_half = rock - (first_half * factor)
            eval_result = [first_half, second_half]
        else:
            eval_result = [rock * 2024]
    return eval_result


def read_parse():
    with open('input') as f:
        data = f.read()
    return list(map(int, data.strip().split(' ')))


if __name__ == '__main__':
    assert eval_rock(0) == [1]
    assert eval_rock(9) == [9 * 2024]
    assert eval_rock(10) == [1, 0]
    assert eval_rock(11) == [1, 1]
    assert count_eval_rock(0, 2) == len([2024])
    assert count_eval_rock(0, 3) == len([20, 24])
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
