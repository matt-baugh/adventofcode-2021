from pathlib import Path
import math

import numpy as np
import torch
import torch.nn.functional as F
from tqdm import tqdm

from utils.file_utils import load_file

PRINT = False


def calc_completion_steps(rock_map: torch.Tensor, start_pos: tuple[int, int]) -> list[int]:
    step_map = torch.zeros_like(rock_map)
    step_map[start_pos] = 1

    step_kernel = torch.Tensor([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

    rock_map = rock_map.unsqueeze(0).unsqueeze(0)
    step_map = step_map.unsqueeze(0).unsqueeze(0)
    step_kernel = step_kernel.unsqueeze(0).unsqueeze(0)
    last_step_map = None
    last_last_step_map = None

    step_sums = [1]

    while last_last_step_map is None or not torch.equal(last_last_step_map, step_map):
        last_last_step_map = last_step_map
        last_step_map = step_map.clone()
        step_map = F.conv2d(step_map, step_kernel, padding=1)
        step_map[rock_map == 1] = 0
        step_map[step_map > 0] = 1
        step_sums.append(step_map.sum().item())

    return step_sums[:-1]


def calc_num_locs_in_dir(remaining_steps: int, step_sums: list[int], axis_gap: int) -> int:

    num_maps_curr_dir = remaining_steps / axis_gap
    if num_maps_curr_dir.is_integer():
        num_maps_curr_dir += 1
    else:
        num_maps_curr_dir = math.ceil(num_maps_curr_dir)

    total_locs = 0
    fully_covered_steps = (
        remaining_steps - (len(step_sums) - 1)) // axis_gap
    fully_covered_steps = max(fully_covered_steps, 0)

    even_num_locs = step_sums[-1 -
                              (remaining_steps - len(step_sums)) % 2]
    odd_num_locs = step_sums[-1 -
                             (remaining_steps - axis_gap - len(step_sums)) % 2]
    total_locs += fully_covered_steps // 2 * \
        (even_num_locs + odd_num_locs)
    total_locs += fully_covered_steps % 2 * even_num_locs

    for i in range(fully_covered_steps, num_maps_curr_dir):
        curr_remaining_steps = remaining_steps - i * axis_gap
        if curr_remaining_steps >= len(step_sums):
            total_locs += step_sums[-1 -
                                    (curr_remaining_steps - len(step_sums)) % 2]
        elif curr_remaining_steps >= 0:
            total_locs += step_sums[-1 - curr_remaining_steps % 2]

    return total_locs


def calc_num_locations(filename: str, num_steps: int) -> int:

    raw_input = load_file(Path(__file__).parent / filename)

    rock_map = torch.Tensor(
        [[1 if c == '#' else 0 for c in line] for line in raw_input])

    start_pos = [(i, j) for i, r in enumerate(raw_input)
                 for j, c in enumerate(r) if c == 'S']
    assert len(start_pos) == 1
    start_pos = start_pos[0]

    centre_step_sums = calc_completion_steps(rock_map, start_pos)
    assert centre_step_sums[0] == 1, centre_step_sums[0]
    assert centre_step_sums[-1] == 7770, centre_step_sums[-1]
    assert centre_step_sums[-2] == 7627, centre_step_sums[-2]

    # Check known clear paths (the border of the map, and centre lines)
    assert torch.all(rock_map[0, :] == 0)
    assert torch.all(rock_map[-1, :] == 0)
    assert torch.all(rock_map[:, 0] == 0)
    assert torch.all(rock_map[:, -1] == 0)
    assert torch.all(rock_map[start_pos[0], :] == 0)
    assert torch.all(rock_map[:, start_pos[1]] == 0)

    vertical_centre_gap = rock_map.shape[0]
    horizontal_centre_gap = rock_map.shape[1]

    print('horizontal_centre_gap: ', horizontal_centre_gap)
    print('vertical_centre_gap: ', vertical_centre_gap)

    # Calculate all other step sums
    step_sums_from_left = calc_completion_steps(rock_map, (start_pos[0], 0))
    step_sums_from_bottom_left = calc_completion_steps(rock_map, (-1, 0))
    step_sums_from_top_left = calc_completion_steps(rock_map, (0, 0))

    step_sums_from_right = calc_completion_steps(rock_map, (start_pos[0], -1))
    step_sums_from_bottom_right = calc_completion_steps(rock_map, (-1, -1))
    step_sums_from_top_right = calc_completion_steps(rock_map, (0, -1))

    step_sums_from_bottom = calc_completion_steps(rock_map, (-1, start_pos[1]))
    step_sums_from_top = calc_completion_steps(rock_map, (0, start_pos[1]))

    print('All step sums calculated')

    # Start working out total number of reachable locations

    total_locs = centre_step_sums[-1 -
                                  (num_steps - (len(centre_step_sums) - 1)) % 2]

    # Maps on centre line
    for (axis_start_pos, axis_gap, axis_step_lists) in [(start_pos[1], horizontal_centre_gap, [step_sums_from_left, step_sums_from_right]),
                                                        (start_pos[0], vertical_centre_gap, [step_sums_from_bottom, step_sums_from_top])]:

        remaining_steps = num_steps - (axis_start_pos + 1)
        for curr_step_list in axis_step_lists:
            total_locs += calc_num_locs_in_dir(
                remaining_steps, curr_step_list, axis_gap)

    print('All centre line step sums calculated - ', total_locs)
    assert total_locs == 6229633827
    # Maps in corners
    remaining_steps = num_steps - (start_pos[0] + 1) - (start_pos[1] + 1)
    max_hor_maps = remaining_steps / horizontal_centre_gap
    if max_hor_maps.is_integer():
        max_hor_maps += 1
    else:
        max_hor_maps = math.ceil(max_hor_maps)


    # TODO: calculate this with a floor + only iterate for the remainder
    for i in tqdm(range(max_hor_maps), 'Calculating corner step sums'):

        row_remaining_steps = remaining_steps - i * horizontal_centre_gap

        for curr_step_list in [step_sums_from_bottom_left, step_sums_from_bottom_right, step_sums_from_top_left, step_sums_from_top_right]:
            total_locs += calc_num_locs_in_dir(
                row_remaining_steps, curr_step_list, vertical_centre_gap)

    return total_locs
    


if __name__ == "__main__":
    # test_sol = calc_num_locations("data1_test.txt", 50)
    # print(test_sol)
    # assert test_sol == 1594
    # test_sol = calc_num_locations("data1_test.txt", 100)
    # print(test_sol)
    # assert test_sol == 6536
    # test_sol = calc_num_locations("data1_test.txt", 500)
    # print(test_sol)
    # assert test_sol == 167004
    # test_sol = calc_num_locations("data1_test.txt", 1000)
    # print(test_sol)
    # assert test_sol == 668697
    # test_sol = calc_num_locations("data1_test.txt", 5000)
    # print(test_sol)
    # assert test_sol == 16733044
    real_sol = calc_num_locations("data1_real.txt", 26501365)
    print(real_sol)
