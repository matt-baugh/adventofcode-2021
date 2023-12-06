import math
from pathlib import Path

from utils.file_utils import parse_file_lines


def multply_boat_solutions(filename: str):
    parsed_input = parse_file_lines(
        Path(__file__).parent / filename, split_val=None)
    assert len(parsed_input) == 2

    race_times = [int(x) for x in parsed_input[0][1:]]
    race_targets = [int(x) for x in parsed_input[1][1:]]

    race_sol_prod = 1
    for r_time, r_target in zip(race_times, race_targets):
        # t: int, 0 < t < r_target
        # d = (r_time - t) * t
        # d > r_target
        # (r_time - t) * t > r_target
        # r_time * t - t^2 > r_target
        # t^2 - r_time * t + r_target < 0

        sqrt_quad_det = (r_time ** 2 - 4 * r_target) ** 0.5

        min_time = (r_time - sqrt_quad_det) / 2
        max_time = (r_time + sqrt_quad_det) / 2
        
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

        race_sol_prod *= num_int_sols

    return race_sol_prod


if __name__ == "__main__":
    test_sol = multply_boat_solutions("data1_test.txt")
    print(test_sol)
    assert test_sol == 288
    print(multply_boat_solutions("data1_real.txt"))
