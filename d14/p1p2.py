import math
import re
import timeit


def p1():
    robots, max_xy = read_parse()
    ticks = 100
    # print_grid(robots, max_xy)
    for tick in range(ticks):
        for robot_i in range(len(robots)):
            robots[robot_i] = iter_robot(robots[robot_i], max_xy)
        # print_grid(robots, max_xy)
    quad_x = max_xy[0] // 2
    quad_y = max_xy[1] // 2
    # First xy is top-left inclusive, second xy is bottom-right exclusive.
    quad_bounds = [
        ((0, 0), (quad_x, quad_y)), # NW
        ((quad_x + 1, 0), (quad_x + 1 + quad_x, quad_y)), # NE
        ((quad_x + 1, quad_y + 1), (quad_x + 1 + quad_x, quad_y + 1 + quad_y)), # SE
        ((0, quad_y + 1), (quad_x, quad_y + 1 + quad_y)), # SW
    ]
    # print_grid(robots, max_xy, quad_bounds)
    quad_counts = [0] * len(quad_bounds)
    for robot in robots:
        for quad_i, quad in enumerate(quad_bounds):
            if in_bounds(robot, quad):
                quad_counts[quad_i] += 1
                break

    score = 1
    for count in quad_counts:
        score *= count
    print(score)


def p2():
    robots, max_xy = read_parse()
    ticks = max_xy[0] * max_xy[1]
    robot_x_std_devs = []
    robot_y_std_devs = []
    robot_x_std_devs.append(sample_std_dev([rp[0] for rp in robots])[1])
    robot_y_std_devs.append(sample_std_dev([rp[1] for rp in robots])[1])
    for tick in range(ticks):
        for robot_i in range(len(robots)):
            robots[robot_i] = iter_robot(robots[robot_i], max_xy)
        robot_x_std_devs.append(sample_std_dev([rp[0] for rp in robots])[1])
        robot_y_std_devs.append(sample_std_dev([rp[1] for rp in robots])[1])
    # This probalby isn't valid statistically, but it seems to work
    outlier_xs = find_outliers(robot_x_std_devs, threshold=6)
    outlier_ys = find_outliers(robot_y_std_devs, threshold=6)
    intersections = set(outlier_xs).intersection(set(outlier_ys))
    assert len(intersections) == 1
    ticks = intersections.pop()
    for tick in range(ticks):
        for robot_i in range(len(robots)):
            robots[robot_i] = iter_robot(robots[robot_i], max_xy)
    print_grid(robots, max_xy)
    print(f'p2: {ticks}')


def iter_robot(rp, max_xy):
    new_rp = (
        (rp[0] + rp[2]) % max_xy[0],  # new_x = (old_x + vx) % max_x
        (rp[1] + rp[3]) % max_xy[1],  # new_y = (old_y + vy) % max_y
        rp[2],  # Same velocity
        rp[3],  # Same velocity
    )
    return new_rp


def in_bounds(rp, bounds):
    return (
            bounds[0][0] <= rp[0] < bounds[1][0] and  # left <= X < right
            bounds[0][1] <= rp[1] < bounds[1][1]  # top <= Y < bottom
    )


def print_grid(robots, max_xy, quad_bounds=None):
    output = ''
    for y in range(max_xy[1]):
        for x in range(max_xy[0]):
            if quad_bounds is not None and all((not in_bounds((x, y, 0, 0), bound) for bound in quad_bounds)):
                output += '#'
                continue
            count = 0
            for robot in robots:
                if in_bounds(robot, ((x, y), (x + 1, y + 1))):
                    count += 1
            if count > 0:
                output += str(count)
            else:
                output += '.'
        output += '\n'
    print(output)


def sample_std_dev(samples):
    # Calculate mean of the sample
    mean = sum(samples) / len(samples)

    # Calculate standard deviation of the sample
    variance = sum((x - mean) ** 2 for x in samples) / len(samples)
    std_deviation = variance ** 0.5
    return mean, std_deviation


def calculate_z_score(samples):
    mean, std_dev = sample_std_dev(samples)

    # Calculate Z-score for each value in the sample
    z_scores = [(x - mean) / std_dev for x in samples]

    return z_scores


def find_outliers(samples, threshold: float=3):
    z_scores = calculate_z_score(samples)
    outliers = [i for i, z in enumerate(z_scores) if math.fabs(z) > threshold]
    return outliers


def read_parse():
    with open('input') as f:
        lines = f.readlines()
    robots = []
    for line in lines:
        x, y, vx, vy = map(int, re.findall(r'(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+)$', line)[0])
        robots.append((x, y, vx, vy))
    # max_xy = (11, 7)
    max_xy = (101, 103)
    return robots, max_xy


if __name__ == '__main__':
    print(f'p1: {timeit.timeit(p1, number=1)}')
    print(f'p2: {timeit.timeit(p2, number=1)}')
