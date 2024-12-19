from time import time

from task1 import count_possible_combinations
from utils.file_utils import load_file, chunk_input


def count_all_combinations(filename_str: str) -> int:

    content = load_file(filename_str)

    towel_inputs, pattern_inputs = chunk_input(content, "")

    all_towels = towel_inputs[0].split(", ")
    towel_map = {}

    for towel in all_towels:
        if towel[0] not in towel_map:
            towel_map[towel[0]] = []
        towel_map[towel[0]].append(towel)

    possible_combinations = 0
    previous_patterns = {"": 1}

    for pattern in pattern_inputs:
        possible_combinations += count_possible_combinations(
            pattern, towel_map, previous_patterns)

    return possible_combinations


if __name__ == "__main__":

    test_res = count_all_combinations("data1_test.txt")
    assert test_res == 16, f"Test failed: {test_res}"
    start = time()
    print(count_all_combinations("data1_real.txt"))
    print("Execution time:", time() - start)
