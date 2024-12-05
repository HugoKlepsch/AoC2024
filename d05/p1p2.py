import functools
import re
import typing


def p1():
    constraints, page_lists = read_parse()
    k_after_any_v_map: typing.Dict[int, typing.Set[int]] = build_constraints(constraints)

    score = 0
    for page_list in page_lists:
        if is_correct(page_list, k_after_any_v_map):
            score += page_list[len(page_list) // 2]

    print(score)


def p2():
    constraints, page_lists = read_parse()
    k_after_any_v_map: typing.Dict[int, typing.Set[int]] = build_constraints(constraints)
    score = 0
    for page_list in page_lists:
        if not is_correct(page_list, k_after_any_v_map):
            new_list = sorted(page_list, key=functools.cmp_to_key(lambda x, y: -1 if x in k_after_any_v_map.get(y, []) else 1))
            while not is_correct(new_list, k_after_any_v_map):
                new_list = sorted(new_list, key=functools.cmp_to_key(lambda x, y: -1 if x in k_after_any_v_map.get(y, []) else 1))
            score += new_list[len(new_list) // 2]

    print(score)


def build_constraints(constraints: typing.List[typing.Tuple[int, int]]) -> typing.Dict[int, typing.Set[int]]:
    k_after_any_v_map: typing.Dict[int, typing.Set[int]] = {}
    for constraint in constraints:
        if constraint[1] in k_after_any_v_map:
            k_after_any_v_map[constraint[1]].add(constraint[0])
        else:
            k_after_any_v_map[constraint[1]] = {constraint[0]}
    return k_after_any_v_map


def is_correct(page_list: typing.List[int], k_after_any_v_map: typing.Dict[int, typing.Set[int]]) -> bool:
    for page_i, page in enumerate(page_list):
        must_not_appear_after_page = k_after_any_v_map.get(page, [])
        for other_page in page_list[page_i+1:]:
            if other_page in must_not_appear_after_page:
                # We found another page that should have come before this one, but it came after. Fail the page_list
                return False
    return True


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    parse_stage = 0
    constraints: typing.List[typing.Tuple[int, int]] = []  # stage 0
    page_lists: typing.List[typing.List[int]] = []  # stage 1
    for line in lines:
        if line == "\n":
            parse_stage = 1
            continue
        if parse_stage == 0:
            numbers = [int(x) for x in re.findall(r'\d+', line)]
            assert len(numbers) == 2
            constraints.append((numbers[0], numbers[1]))
        elif parse_stage == 1:
            page_lists.append([int(x) for x in re.findall(r'\d+', line)])
    return constraints, page_lists


if __name__ == '__main__':
    p1()
    p2()