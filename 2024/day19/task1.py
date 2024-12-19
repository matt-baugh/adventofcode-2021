from dataclasses import dataclass
from enum import Enum
import re
from time import time


from utils.file_utils import load_file, chunk_input


def count_possible_combinations(pattern: str, towel_map: dict[str, list[str]], previous_patterns: dict[str, int]) -> int:

    possible_combinations = 0

    if pattern[0] not in towel_map:
        return 0

    for t in towel_map[pattern[0]]:
        if pattern.startswith(t):
            remaining_pattern = pattern[len(t):]
            if remaining_pattern in previous_patterns:
                num_combinations = previous_patterns[remaining_pattern]
            else:
                num_combinations = count_possible_combinations(
                    remaining_pattern, towel_map, previous_patterns)
                previous_patterns[remaining_pattern] = num_combinations
            possible_combinations += num_combinations

    return possible_combinations


def count_possible_designs(filename_str: str) -> int:

    content = load_file(filename_str)

    towel_inputs, pattern_inputs = chunk_input(content, "")

    all_towels = towel_inputs[0].split(", ")
    towel_map = {}

    for towel in all_towels:
        if towel[0] not in towel_map:
            towel_map[towel[0]] = []
        towel_map[towel[0]].append(towel)

    possible_patterns = 0
    previous_patterns = {"": 1}

    for pattern in pattern_inputs:
        possible_combinations = count_possible_combinations(
            pattern, towel_map, previous_patterns)
        if possible_combinations >= 1:
            possible_patterns += 1

    return possible_patterns


if __name__ == "__main__":

    test_res = count_possible_designs("data1_test.txt")
    assert test_res == 6, f"Test failed: {test_res}"
    start = time()
    print(count_possible_designs("data1_real.txt"))
    print("Execution time:", time() - start)
