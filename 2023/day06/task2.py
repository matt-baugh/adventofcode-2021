import math
from pathlib import Path

from utils.file_utils import parse_file_lines


def multply_boat_solutions(filename: str):
    parsed_input = parse_file_lines(
        Path(__file__).parent / filename, split_val=None)
    assert len(parsed_input) == 2

    race_time = int(''.join(parsed_input[0][1:]))
    race_target = int(''.join(parsed_input[1][1:]))

    # t: int, 0 < t < race_target
    # d = (race_time - t) * t
    # d > race_target
    # (race_time - t) * t > race_target
    # race_time * t - t^2 > race_target
    # t^2 - race_time * t + race_target < 0

    sqrt_quad_det = (race_time ** 2 - 4 * race_target) ** 0.5

    min_time = (race_time - sqrt_quad_det) / 2
    max_time = (race_time + sqrt_quad_det) / 2

    if min_time % 1 == 0:
        min_time += 1
    else:
        min_time = math.ceil(min_time)

    if max_time % 1 == 0:
        max_time -= 1
    else:
        max_time = math.floor(max_time)
    num_int_sols = max_time - min_time + 1
    print(min_time, max_time, num_int_sols)

    return num_int_sols


if __name__ == "__main__":
    test_sol = multply_boat_solutions("data1_test.txt")
    print(test_sol)
    assert test_sol == 71503
    print(multply_boat_solutions("data1_real.txt"))
