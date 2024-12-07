import dataclasses
import itertools
import math
from typing import Callable, Set, List
import timeit


@dataclasses.dataclass
class Operator:
    name: str
    func: Callable
    def __hash__(self) -> int:
        return hash(self.name)


def p1():
    calibrations = read_parse()
    operators: Set[Operator] = {
        Operator('+', lambda a, b: a + b),
        Operator('*', lambda a, b: a * b),
    }

    score = 0
    for calibration in calibrations:
        target = calibration[0]
        elements = calibration[1]
        if can_solve_by_applying_operators(target, elements, operators):
            score += target

    print(score)


def p2(concat_func: int):
    calibrations = read_parse()
    def _concat1(a: int, b: int) -> int:
        return int(f'{a}{b}')
    def _concat2(a: int, b: int) -> int:
        num_digits = math.ceil(math.log10(b))
        a = a * 10 ** num_digits
        return a + b
    concat_funcs = [
        _concat1,
        _concat2,
    ]
    operators: Set[Operator] = {
        Operator('+', lambda a, b: a + b),
        Operator('*', lambda a, b: a * b),
        Operator('||', concat_funcs[concat_func]),
    }

    score = 0
    for calibration in calibrations:
        target = calibration[0]
        elements = calibration[1]
        if can_solve_by_applying_operators(target, elements, operators):
            score += target

    print(score)


def can_solve_by_applying_operators(target: int, elements: List[int], operators: Set[Operator]) -> bool:
    # Try a combination of operators until one works
    bs = [elements[x] for x in range(1, len(elements))]
    for operator_set in itertools.product(operators, repeat=len(elements)-1):
        assert len(operator_set) == len(bs)
        accumulator = elements[0]
        for operator, b in zip(operator_set, bs):
            if accumulator > target:
                # already too high, skip
                break
            accumulator = operator.func(accumulator, b)
        if accumulator == target:
            return True
    return False


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    calibrations = []
    for line in lines:
        segments = line.split(':')
        target = int(segments[0])
        elements = list(map(int, segments[1].strip().split(' ')))
        calibrations.append((target, elements))
    return calibrations


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=3)}')
    print(f'p2_0: {timeit.timeit(lambda: p2(0), number=3)}')
    print(f'p2_1: {timeit.timeit(lambda: p2(1), number=3)}')
