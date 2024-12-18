from time import time

from utils.file_utils import load_file
from task1 import compute_path_len


def find_first_blockage(filename_str: str, board_size: int) -> tuple[int, int]:
    content = load_file(filename_str)

    falling_blocks = [tuple(int(i) for i in l.split(','))for l in content]

    # Binary search to find the first blockage
    lower = 0
    upper = len(falling_blocks)
    while lower < upper:
        num_blocks_fallen = (lower + upper) // 2
        path_len = compute_path_len(
            set(falling_blocks[:num_blocks_fallen]), board_size)

        if path_len is None:
            upper = num_blocks_fallen
        else:
            lower = num_blocks_fallen + 1

    # Need to return the blockage that caused the path to be blocked (final element of list that failed to find path)
    return falling_blocks[lower - 1]


if __name__ == "__main__":

    test_res = find_first_blockage("data1_test.txt", 7)
    assert test_res == (6, 1), f"Test failed: {test_res}"
    start = time()
    print(find_first_blockage("data1_real.txt", 71))
    print("Execution time:", time() - start)
