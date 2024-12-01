from itertools import product
from pathlib import Path
import math

import numpy as np
import torch
import torch.nn.functional as F
from tqdm import tqdm

from utils.file_utils import load_file

PRINT = True

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

ALL_DIRS = [NORTH, EAST, SOUTH, WEST]


def get_coords_towards(coords: list[tuple[int, int]], direction: int):
    axis = direction % 2
    relevant_coords = [c[axis] for c in coords]
    select_fn = max if direction in [EAST, SOUTH] else min
    target_coord = select_fn(relevant_coords)
    return [c for c in coords if c[axis] == target_coord]


def calc_completion_steps(rock_map: torch.Tensor, input_positions: tuple[tuple[int, tuple[tuple[int, int], ...]], ...]) \
        -> tuple[list[int], dict[tuple[int, int], int]]:
    step_map = torch.zeros_like(rock_map)

    assert input_positions[0][0] == 0

    step_kernel = torch.Tensor([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

    rock_map = rock_map.unsqueeze(0).unsqueeze(0)
    step_map = step_map.unsqueeze(0).unsqueeze(0)
    step_kernel = step_kernel.unsqueeze(0).unsqueeze(0)
    last_step_map = None
    last_last_step_map = None
    loc_distances = {}
    step_sums = []

    while last_last_step_map is None or not torch.equal(last_last_step_map, step_map):
        last_last_step_map = last_step_map
        last_step_map = step_map.clone()
        step_map = F.conv2d(step_map, step_kernel, padding=1)

        steps_taken = len(step_sums)
        if len(input_positions) > 0 and steps_taken == input_positions[0][0]:
            for p in input_positions[0][1]:
                step_map[0, 0, p[0], p[1]] = 1
            input_positions = input_positions[1:]

        step_map[rock_map == 1] = 0
        step_map[step_map > 0] = 1

        for c in torch.argwhere(step_map[0, 0]):
            tuple_c = tuple(c.numpy())
            if tuple_c not in loc_distances:
                loc_distances[tuple_c] = steps_taken
        step_sums.append(step_map.sum().item())

    return step_sums[:-1], loc_distances


def calc_num_locs_in_dir(remaining_steps: int, step_sums: list[int], axis_gap: int) -> int:

    num_maps_curr_dir = remaining_steps / axis_gap
    if num_maps_curr_dir.is_integer():
        num_maps_curr_dir += 1
    else:
        num_maps_curr_dir = math.ceil(num_maps_curr_dir)
    num_maps_curr_dir = int(num_maps_curr_dir)

    total_locs = 0
    fully_covered_steps = (
        remaining_steps - (len(step_sums) - 1 - axis_gap)) // axis_gap
    fully_covered_steps = max(fully_covered_steps, 0)

    curr_step_remainder = (remaining_steps - len(step_sums)) % 2
    even_num_locs = step_sums[-2 + curr_step_remainder]
    odd_num_locs = step_sums[-1 - curr_step_remainder]
    total_locs += fully_covered_steps // 2 * \
        (even_num_locs + odd_num_locs)
    total_locs += fully_covered_steps % 2 * even_num_locs
    # fully_covered_steps = (fully_covered_steps // 2) * 2

    for i in range(fully_covered_steps, num_maps_curr_dir):
        curr_remaining_steps = remaining_steps - i * axis_gap
        if curr_remaining_steps >= len(step_sums):
            total_locs += step_sums[-1 -
                                    (curr_remaining_steps - len(step_sums)) % 2]
        elif curr_remaining_steps >= 0:
            total_locs += step_sums[curr_remaining_steps]

    return total_locs


# Consider the map (with X as start)
# .....    .....    X....    .X...    X.X..    .X.X.    X.X.X
# .##..    X##..    .##..    X##..    .##X.    X##.X    .##X.
# X.... -> .X... -> X.X.. -> .X.X. -> X.X.X -> .X.X. -> X.X.X
# ..##.    X.##.    .X##.    X.##.    .X##.    X.##X    .X##.
# .....    .....    X....    .X...    X.X..    .X.X.    X.X.X
#
# 1        3        5        6        9        10       11
test_map1 = torch.Tensor([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]])

expected_step_sums1 = [1, 3, 5, 6, 9, 10, 11]
expected_loc_dists1 = {
    (2, 0): 0,
    (1, 0): 1,
    (2, 1): 1,
    (3, 0): 1,
    (0, 0): 2,
    (2, 2): 2,
    (3, 1): 2,
    (4, 0): 2,
    (0, 1): 3,
    (2, 3): 3,
    (4, 1): 3,
    (0, 2): 4,
    (1, 3): 4,
    (2, 4): 4,
    (4, 2): 4,
    (0, 3): 5,
    (1, 4): 5,
    (3, 4): 5,
    (4, 3): 5,
    (0, 4): 6,
    (4, 4): 6
}

test_step_sums1, test_loc_dists1 = calc_completion_steps(
    test_map1, ((0, ((2, 0),)),))
assert len(test_step_sums1) == len(
    expected_step_sums1), f'Expected {expected_step_sums1}, returned {test_step_sums1}'
for ss_i, (ss1, e_ss1) in enumerate(zip(test_step_sums1, expected_step_sums1)):
    assert ss1 == e_ss1, f'Mismatch at {ss_i}: exp. {e_ss1}, ret {ss1}'

assert len(test_loc_dists1) == len(expected_loc_dists1), \
    f'Expected {expected_loc_dists1}, returned {test_loc_dists1}'
for k, exp_d in expected_loc_dists1.items():
    assert test_loc_dists1[k] == exp_d, \
        f'Mismatch at key {k}: exp. {exp_d}, returned {test_loc_dists1[k]}'

test_axis_gap = 5

# Test expected results:
# 7: 10 + 5 = 15
# 9: 10 + 9 = 19
# 10: 11 + 10 + 1 = 22
# 11: 10 + 11 + 3 = 24
# 20: 11 + 10 + 11 + 10 + 1 = 43
for test_num_steps, exp_num_locs in [(0, 1), (2, 5), (4, 9), (5, 11), (7, 15), (9, 19), (10, 22), (11, 24), (12, 26),
                                     (20, 43)]:
    test_num_locs = calc_num_locs_in_dir(
        test_num_steps, test_step_sums1, test_axis_gap)
    assert test_num_locs == exp_num_locs, f'For {test_num_steps}: expected {exp_num_locs}, got {test_num_locs}'


def distance_map_to_str(loc_distances: dict[tuple[int, int], int], map_shape: tuple[int, int]) -> str:
    dist_map = np.zeros(map_shape) - 1

    for c, dist in loc_distances.items():
        dist_map[c] = dist

    return str(dist_map)


def wrap_coord(coord: tuple[int, int], map_size: tuple[int, int], direction: int) -> tuple[int, int]:
    dir_axis = direction % 2
    dir_coord = coord[dir_axis]
    if direction in [NORTH, WEST]:
        assert dir_coord == 0
        new_dir_coord = map_size[dir_axis] - 1
    else:
        assert dir_coord == map_size[dir_axis] - 1
        new_dir_coord = 0
    return tuple(new_dir_coord if i == dir_axis else v for i, v in enumerate(coord))


def calc_num_locations(filename: str, num_steps: int) -> int:

    raw_input = load_file(Path(__file__).parent / filename)

    rock_map = torch.Tensor(
        [[1 if c == '#' else 0 for c in line] for line in raw_input])

    start_pos = [(i, j) for i, r in enumerate(raw_input)
                 for j, c in enumerate(r) if c == 'S']
    assert len(start_pos) == 1
    start_pos = start_pos[0]

    # Check known clear paths (the border of the map, and centre lines)
    assert torch.all(rock_map[0, :] == 0)
    assert torch.all(rock_map[-1, :] == 0)
    assert torch.all(rock_map[:, 0] == 0)
    assert torch.all(rock_map[:, -1] == 0)
    # assert torch.all(rock_map[start_pos[0], :] == 0)
    # assert torch.all(rock_map[:, start_pos[1]] == 0)

    vertical_centre_gap = rock_map.shape[0]
    horizontal_centre_gap = rock_map.shape[1]

    print('horizontal_centre_gap: ', horizontal_centre_gap)
    print('vertical_centre_gap: ', vertical_centre_gap)

    start_pos_seed = ((0, (start_pos,)),)
    centre_step_sums, dists_from_centre = calc_completion_steps(
        rock_map, start_pos_seed)
    assert centre_step_sums[0] == 1, centre_step_sums[0]
    # assert centre_step_sums[-1] == 7770, centre_step_sums[-1]
    # assert centre_step_sums[-2] == 7627, centre_step_sums[-2]

    # Calculate all other step sums
    corner_coords = list(
        product([0, vertical_centre_gap - 1], [0, horizontal_centre_gap - 1]))
    start_to_infos = {}
    for curr_start in corner_coords:
        curr_corner_seed = ((0, (curr_start,)),)
        start_to_infos[curr_start] = calc_completion_steps(
            rock_map, curr_corner_seed)

    total_locs = calc_locs_covered(num_steps, centre_step_sums)
    if PRINT:
        print('Total locs in central map: ', total_locs)

    accessible_coords = list(dists_from_centre.keys())

    for d in ALL_DIRS:
        min_dist_in_dir, curr_seed_coords = get_min_dist_in_dir(
            dists_from_centre, accessible_coords, d, rock_map.shape)

        assert curr_seed_coords is not [], 'How could this be empty?'

        if curr_seed_coords not in start_to_infos:
            start_to_infos[curr_seed_coords] = calc_completion_steps(
                rock_map, curr_seed_coords)

        # Minus 1 as we step onto the new map
        curr_remaining_steps = num_steps - (min_dist_in_dir + 1)

        if PRINT:
            print()
            print(f'Going {d} from {start_pos} to {coords_with_min_dist[0]}')
            print(
                f'Initially we have {curr_remaining_steps} steps left, starting at {curr_seed_coords}')

        if curr_remaining_steps < 0:
            continue

        curr_dir_step_sums, curr_dir_dist_map = start_to_infos[curr_seed_coords]

        # TODO: instead of checking for wrapped_coord in wrapped_min_dist_coords,
        # check if seed coords is unchanged
        min_dist_in_dir, coords_with_min_dist = get_min_dist_in_dir(
            curr_dir_dist_map, accessible_coords, d, rock_map.shape)
        wrapped_min_dist_coords = [wrap_coord(
            c, rock_map.shape, d) for c in coords_with_min_dist]

        # Aim to find part where coords loop
        while wrapped_coord not in wrapped_min_dist_coords and curr_remaining_steps >= 0:

            new_locs = calc_locs_covered(curr_remaining_steps,
                                         curr_dir_step_sums)
            if PRINT:
                print(f'Adding {new_locs} locs from {wrapped_coord}')
            total_locs += new_locs
            assert len(wrapped_min_dist_coords) == 1

            wrapped_coord = wrapped_min_dist_coords[0]
            if wrapped_coord not in start_to_infos:
                start_to_infos[wrapped_coord] = calc_completion_steps(
                    rock_map, wrapped_coord)

            curr_remaining_steps -= min_dist_in_dir + 1
            curr_dir_step_sums, curr_dir_dist_map = start_to_infos[wrapped_coord]
            min_dist_in_dir, coords_with_min_dist = get_min_dist_in_dir(
                curr_dir_dist_map, accessible_coords, d, rock_map.shape)
            wrapped_min_dist_coords = [wrap_coord(
                c, rock_map.shape, d) for c in coords_with_min_dist]

        if curr_remaining_steps < 0:
            continue

        new_looping_locs = calc_num_locs_in_dir(
            curr_remaining_steps, curr_dir_step_sums, min_dist_in_dir + 1)
        print(f'Found cycle, adding {new_looping_locs} locs')
        total_locs += new_looping_locs

    return total_locs

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


def calc_locs_covered(num_steps, step_sums):
    if num_steps < len(step_sums):
        return step_sums[num_steps]
    else:
        return step_sums[-2 + ((num_steps - len(step_sums)) % 2)]


def get_min_dist_in_dir(dists_from_centre, accessible_coords, d, map_size):
    coords_in_dir = get_coords_towards(accessible_coords, d)
    coords_in_dir_distances = {d: dists_from_centre[d] for d in coords_in_dir}
    min_dist_in_dir = min(coords_in_dir_distances.values())

    seed_coords = []
    for dist in sorted(coords_in_dir_distances.values()):
        offset_dist = dist - min_dist_in_dir
        wrapped_coords = [wrap_coord(c, map_size, d)
                          for c, c_d in coords_in_dir_distances.items() if c_d == dist]
        seed_coords.append((offset_dist, sorted(wrapped_coords)))
    return min_dist_in_dir, tuple(seed_coords)


if __name__ == "__main__":

    test_sol = calc_num_locations("data1_test.txt", 6)
    print(test_sol)
    assert test_sol == 16
    test_sol = calc_num_locations("data1_test.txt", 9)
    # expect 29 in middle
    # 1 directly up
    # 1 directly right
    # 3 directly below
    # 7 to left
    # 41 total
    print(test_sol)
    assert test_sol == 41
    test_sol = calc_num_locations("data1_test.txt", 50)
    print(test_sol)
    assert test_sol == 1594
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
    # 630136005648599 - too high
    # 630135947791371 - wrong, unknown
    # 630136005648599.0
