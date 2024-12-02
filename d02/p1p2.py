import math
from math import fabs

def p1():
    reports = read_parse()

    score = 0
    for report in reports:
        if check_safe(report):
            score += 1

    print(score)


def p2():
    reports = read_parse()

    score = 0
    for report in reports:
        if check_safe(report):
            score += 1
        else:
            # Try again after removing an element
            for e_to_remove in range(len(report)):
                new_report = report[:e_to_remove] + report[e_to_remove+1:]
                if check_safe(new_report):
                    score += 1
                    break

    print(score)


def check_safe(report) -> bool:
    min_diff, max_diff = min_max_diff(report)
    if (all_increasing(report) or all_decreasing(report)) and min_diff >= 1 and max_diff <= 3:
        return True
    return False


def all_increasing(report):
    for i in range(1, len(report)):
        if report[i] <= report[i-1]:
            return False
    return True


def all_decreasing(report):
    for i in range(1, len(report)):
        if report[i] >= report[i-1]:
            return False
    return True


def min_max_diff(report):
    min_diff = math.inf
    max_diff = 0
    for i in range(1, len(report)):
        diff = fabs(report[i] - report[i-1])
        min_diff = min(min_diff, diff)
        max_diff = max(max_diff, diff)

    return min_diff, max_diff

def read_parse():
    with open('input') as f:
        lines = f.readlines()
        reports = [[int(e) for e in line.split()] for line in lines]
    return reports


if __name__ == '__main__':
    p1()
    p2()