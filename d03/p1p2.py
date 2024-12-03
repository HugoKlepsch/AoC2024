import re


MUL_MATCHER = re.compile(r'mul\(([0-9]+),([0-9]+)\)')


def p1():
    data = read_parse()
    matches = MUL_MATCHER.findall(data)

    score = 0
    for match in matches:
        score += int(match[0]) * int(match[1])

    print(score)


def p2():
    data = read_parse()
    do_matcher = 'do()'
    dont_matcher = 'don\'t()'
    keep_splitting = True
    good_parts = []
    to_split = data
    while keep_splitting:
        results = to_split.split(dont_matcher, 1)
        if len(results) == 1:
            keep_splitting = False
            good_parts.append(results[0])
            break
        before_dont, after_dont = results[0], results[1]
        good_parts.append(before_dont)
        to_split = after_dont
        results = to_split.split(do_matcher, 1)
        if len(results) == 1:
            keep_splitting = False
            break
        before_do, after_do = results[0], results[1]
        to_split = after_do

    score = 0
    for part in good_parts:
        matches = MUL_MATCHER.findall(part)
        for match in matches:
            score += int(match[0]) * int(match[1])

    print(score)


def read_parse():
    with open('input') as f:
        data = f.read()
    return data


if __name__ == '__main__':
    p1()
    p2()