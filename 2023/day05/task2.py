from pathlib import Path
from time import time

import numpy as np
from tqdm import tqdm

from utils.file_utils import load_file


def map_ranges(input_range: tuple[int, int], mappings: list[tuple[int, int, int]]) -> int:
    # mappings are ordered by start index

    # If no mapping present, assume identity mapping
    in_range_start, in_range_end = input_range

    next_range_start = in_range_start
    output_ranges = []

    for (start_i, end_i, new_start_i) in mappings:

        if in_range_end < start_i:
            break

        if end_i < next_range_start:
            continue

        sub_range_start = max(in_range_start, start_i)
        sub_range_end = min(in_range_end, end_i)

        if sub_range_start != next_range_start:
            output_ranges.append((next_range_start, sub_range_start))

        output_ranges.append(
            (new_start_i + (sub_range_start - start_i), new_start_i + (sub_range_end - start_i)))

        next_range_start = sub_range_end

    if next_range_start < in_range_end:
        output_ranges.append((next_range_start, in_range_end))

    return output_ranges


def sum_scratch_points(filename: str):
    parsed_input = load_file(Path(__file__).parent / filename)

    raw_seeds = [int(s)
                 for s in parsed_input[0].split(":")[1].split() if s.isdigit()]

    print('seeds generated')
    all_maps_input = parsed_input[2:]

    maps = {}
    prop_map = {}

    for curr_map_input in '\n'.join(all_maps_input).split('\n\n'):
        curr_map_input_lines = curr_map_input.split('\n')

        map_name, map_const = curr_map_input_lines[0].split()
        assert map_const == 'map:'

        map_from, _, map_to = map_name.split('-')
        prop_map[map_from] = map_to

        curr_map_maps = [l.split() for l in curr_map_input_lines[1:]]
        curr_map_maps = [(int(s_1), int(s_1) + int(l), int(s_2))
                         for s_2, s_1, l in curr_map_maps]
        curr_map_maps.sort(key=lambda x: x[0])
        maps[(map_from, map_to)] = curr_map_maps

    min_location = np.inf
    all_lowest = []

    for s_s, s_l in tqdm(zip(raw_seeds[::2], raw_seeds[1::2])):

        curr_ranges = [(s_s, s_s + s_l)]

        curr_prop = 'seed'

        while curr_prop != 'location':
            print(curr_ranges)
            curr_prop_mapping = (curr_prop, prop_map[curr_prop])
            curr_map = maps[curr_prop_mapping]
            curr_ranges = [
                new_r for r in curr_ranges for new_r in map_ranges(r, curr_map)]
            curr_prop = prop_map[curr_prop]

        curr_min = min([r[0] for r in curr_ranges])
        if curr_min < min_location:
            min_location = curr_min

        all_lowest.append(curr_min)

    # print(all_lowest)

    return min_location


if __name__ == "__main__":
    # start = time()
    print(sum_scratch_points("data1_test.txt"))
    start = time()
    print(sum_scratch_points("data1_real.txt"))
    print(f"Time taken: {time() - start}")
