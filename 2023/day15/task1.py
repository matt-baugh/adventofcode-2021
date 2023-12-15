from functools import reduce
from pathlib import Path

from utils.file_utils import parse_file_lines

PRINT = False


def hash_algorithm(h: str):
    return reduce(lambda acc, v: ((acc + ord(v)) * 17) % 256, h, 0)


def sum_hash_values(filename: str) -> int:
    hash_strs = parse_file_lines(Path(__file__).parent / filename, ',')[0]
    return sum(hash_algorithm(h) for h in hash_strs)


if __name__ == "__main__":
    test_sol = sum_hash_values("data1_test.txt")
    print(test_sol)
    assert test_sol == 1320
    real_sol = sum_hash_values("data1_real.txt")
    print(real_sol)
    assert real_sol == 513643
