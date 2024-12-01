from math import fabs

def p1():
    left, right = read_parse()

    score = 0
    for pair in zip(left, right):
        score += fabs(pair[0] - pair[1])

    print(score)


def p2():
    left, right = read_parse()

    score = 0
    for pair in zip(left, right):
        number = pair[0]
        count = 0
        for r in right:
            if number == r:
                count += 1
        score += number * count

    print(score)


def read_parse():
    with open('input') as f:
        lines = f.readlines()
        numbers = [[int(e) for e in line.split()] for line in lines]
        left = [x[0] for x in numbers]
        right = [x[1] for x in numbers]
        left.sort()
        right.sort()
    return left, right


if __name__ == '__main__':
    p1()
    p2()