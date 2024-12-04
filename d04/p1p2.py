import re


def p1():
    lines = read_parse()

    score = 0
    for line in range(len(lines)):
        for col in range(len(lines[line])):
            score += count_word_occurrences('XMAS', lines, line, col)

    print(score)


def p2():
    lines = read_parse()
    score = 0
    for line in range(len(lines)):
        for col in range(len(lines[line])):
            # Can be any of these:
            #   M.S     S.S     S.M     M.M
            #   .A.     .A.     .A.     .A.
            #   M.S     M.M     S.M     S.S
            if all(
                (
                    # Top left -> down right
                    any((check_for_word(word, lines, line, col, line + 1, col + 1) for word in ['MAS', 'SAM'])),
                    # Bottom left -> top right
                    any((check_for_word(word, lines, line + 2, col, line + 2 - 1, col + 1) for word in ['MAS', 'SAM'])),
                )
            ):
                score += 1

    print(score)


def count_word_occurrences(word, lines, line, col) -> int:
    count = 0

    # Horizontal right
    if check_for_word(word, lines, line, col, line, col + 1):
        count += 1

    # Horizontal left
    if check_for_word(word, lines, line, col, line, col - 1):
        count += 1

    # Vertical up
    if check_for_word(word, lines, line, col, line - 1, col):
        count += 1

    # Vertical down
    if check_for_word(word, lines, line, col, line + 1, col):
        count += 1

    # Diagonal up right
    if check_for_word(word, lines, line, col, line - 1, col + 1):
        count += 1

    # Diagonal down right
    if check_for_word(word, lines, line, col, line + 1, col + 1):
        count += 1

    # Diagonal up left
    if check_for_word(word, lines, line, col, line - 1, col - 1):
        count += 1

    # Diagonal down left
    if check_for_word(word, lines, line, col, line + 1, col - 1):
        count += 1

    return count


def check_for_word(word, lines, line, col, next_line, next_col) -> bool:
    if line < 0 or col < 0 or line >= len(lines) or col >= len(lines[line]):
        return False
    if word[0] == lines[line][col]:
        if len(word) == 1:
            return True
        return check_for_word(word[1:], lines, next_line, next_col, next_line + (next_line - line), next_col + (next_col - col))


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    return lines


if __name__ == '__main__':
    p1()
    p2()