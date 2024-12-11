from functools import cache
import math
from time import time

from utils.file_utils import load_file

stone_dict = {}


@cache
def count_blinks(stone: int, remaining_blinks: int) -> int:

    if stone in stone_dict:
        successors = stone_dict[stone]
    else:
        if stone == 0:
            successors = [1]
        else:
            num_digits = int(math.log10(stone)) + 1
            if num_digits % 2 == 0:
                mid_digit_mod = 10 ** (num_digits // 2)
                successors = [stone // mid_digit_mod, stone % mid_digit_mod]
            else:
                successors = [stone * 2024]

        stone_dict[stone] = successors

    if remaining_blinks == 1:
        return len(successors)

    return sum(count_blinks(stone, remaining_blinks - 1) for stone in successors)


def sum_stones(filename_str: str, blinks: int) -> int:
    content = load_file(filename_str)

    stones = [int(x) for x in content[0].split()]

    return sum(count_blinks(s, blinks) for s in stones)


if __name__ == "__main__":

    print(sum_stones("data1_test.txt", 25))
    start = time()
    print(sum_stones("data1_real.txt", 25))
    print("Execution time:", time() - start)

    start = time()
    print(sum_stones("data1_test.txt", 75))
    print("Execution time 2 test:", time() - start)
    start = time()
    print(sum_stones("data1_real.txt", 75))
    print("Execution time 2 real:", time() - start)
