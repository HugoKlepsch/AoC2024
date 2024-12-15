'''
I (re-)learned solving a system of linear equations using matrices for this.
'''
import re
import timeit
import decimal


def p1():
    machines = read_parse()
    score = 0
    for machine in machines:
        ax, ay, bx, by, px, py = machine[0], machine[1], machine[2], machine[3], machine[4], machine[5]
        score += solve(ax, ay, bx, by, px, py)
    print(score)


def p2():
    machines = read_parse()
    score = 0
    # Need more precision lol
    decimal.getcontext().prec = 50
    for machine in machines:
        ax, ay, bx, by, px, py = machine[0], machine[1], machine[2], machine[3], machine[4], machine[5]
        score += solve(
            decimal.Decimal(ax),
            decimal.Decimal(ay),
            decimal.Decimal(bx),
            decimal.Decimal(by),
            decimal.Decimal(px),
            decimal.Decimal(py),
            offsets=10000000000000
        )
    print(score)


def solve(ax, ay, bx, by, px, py, offsets=0):
    # Create a system of linear equations
    # px = axA + bxB
    # py = ayA + byB
    #
    # Put into matrix form
    # |ax bx| |A| = |px|
    # |ay by| |B| = |py|
    #
    # Isolate |A|
    #         |B|
    # (Find inverse of coefficient matrix)
    # Multiply (coefficient matrix^-1) by constants matrix
    coefficient_m = [
        [ax, bx],
        [ay, by],
    ]
    constants_m = [
        [px],
        [py],
    ]
    constants_m = matrix_scalar_add(constants_m, offsets)
    inverse_coefficients_m = matrix_inverse(coefficient_m)
    solution = matrix_multiply(inverse_coefficients_m, constants_m)

    a = round(solution[0][0])
    b = round(solution[1][0])

    rx = a * ax + b * bx
    ry = a * ay + b * by
    if rx == constants_m[0][0] and ry == constants_m[1][0]:
        return 3*a + b
    else:
        return 0


def matrix_inverse(matrix):
    '''
    Given matrix A, calculate A^-1.
    Only works for 2x2, because I don't know how to do it for anything else
    '''
    a, b, c, d = decompose_2x2(matrix)
    re_shuffled = [
        [d, -b],
        [-c, a]
    ]

    return matrix_scalar_multiply(re_shuffled, 1/matrix_determinate(matrix))


def matrix_determinate(matrix):
    '''
    Given matrix A, calculate its determinant.
    Only works for 2x2, because I don't know how to do it for anything else
    '''
    a, b, c, d = decompose_2x2(matrix)
    return a * d - b * c


def decompose_2x2(matrix):
    assert len(matrix) == 2 and len(matrix[0]) == 2 and len(matrix[1]) == 2
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    return a, b, c, d


def matrix_scalar_add(matrix, scalar):
    '''
    Given matrixes A and number B, calculate A + B.
    '''
    m  = empty_matrix(len(matrix[0]), len(matrix))
    for row in range(len(m)):
        for col in range(len(m[row])):
            m[row][col] = matrix[row][col] + scalar
    return m


def matrix_scalar_multiply(matrix, scalar):
    '''
    Given matrixes A and scalar B, calculate AB.
    '''
    m  = empty_matrix(len(matrix[0]), len(matrix))
    for row in range(len(m)):
        for col in range(len(m[row])):
            m[row][col] = matrix[row][col] * scalar
    return m


def matrix_multiply(matrix_a, matrix_b):
    '''
    Given matrixes A and B, calculate AB.
    '''
    b_height = len(matrix_b)
    assert len(matrix_a[0]) == b_height
    b_width = len(matrix_b[0])
    out = empty_matrix(b_width, b_height)
    out_col_i = 0
    for b_col in range(b_width):
        out_col = []
        for row in range(len(matrix_a)):
            sum = 0
            for col in range(len(matrix_a[row])):
                sum += matrix_a[row][col] * matrix_b[col][b_col]
            out_col.append(sum)
        for i in range(len(out_col)):
            o = out_col[i]
            out[i][out_col_i] = o
        out_col_i += 1
    return out


def empty_matrix(width, height):
    return [[0 for x in range(width)] for y in range(height)]


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    i = 0
    machines = []
    while i < len(lines):
        ax, ay = map(int, re.findall(r'(\d+).*?(\d+)$', lines[i])[0])
        i += 1
        bx, by = map(int, re.findall(r'(\d+).*?(\d+)$', lines[i])[0])
        i += 1
        px, py = map(int, re.findall(r'(\d+).*?(\d+)$', lines[i])[0])
        i += 1
        i += 1
        machines.append((ax, ay, bx, by, px, py))
    return machines


if __name__ == '__main__':
    assert matrix_multiply(
        [
            [1, 2],
            [3, 4]
        ],
        [
            [3],
            [4]
        ],
    ) == [
               [11],
               [25]
           ]
    assert matrix_multiply(
        [
            [1, 2],
            [3, 4]
        ],
        [
            [3, 5],
            [4, 6]
        ],
    ) == [
               [11, 17],
               [25, 39]
           ]
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
