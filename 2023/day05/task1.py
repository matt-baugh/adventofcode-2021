from pathlib import Path
from time import time

import numpy as np

from utils.file_utils import load_file


def map_index(i: int, mappings: list[tuple[int, int, int]]) -> int:
    # mappings are ordered by start index

    # If no mapping present, assume identity mapping
    output_index = i
    for (start_i, end_i, new_start_i) in mappings:
        if i >= start_i and i < end_i:
            output_index = new_start_i + (i - start_i)
            break
        if i < start_i:
            break

    return output_index


def sum_scratch_points(filename: str):
    parsed_input = load_file(Path(__file__).parent / filename)

    seeds = [int(s)
             for s in parsed_input[0].split(":")[1].split() if s.isdigit()]

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
    all_locations = []

    for s in seeds:

        curr_prop = 'seed'

        while curr_prop != 'location':
            curr_prop_mapping = (curr_prop, prop_map[curr_prop])
            curr_map = maps[curr_prop_mapping]
            s = map_index(s, curr_map)
            curr_prop = prop_map[curr_prop]

        if s < min_location:
            min_location = s
        all_locations.append(s)

    # print(all_locations)
    return min_location


if __name__ == "__main__":
    start = time()
    print(sum_scratch_points("data1_test.txt"))
    print(sum_scratch_points("data1_real.txt"))
    print(f"Time taken: {time() - start}")
