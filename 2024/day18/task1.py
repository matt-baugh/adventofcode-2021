from time import time
from typing import Optional

from utils.file_utils import load_file


def compute_path_len(blocks: set[tuple[int, int]], board_size: int) -> Optional[int]:

    start_coord = (0, 0)
    end_coord = (board_size - 1, board_size - 1)

    region_coords = {start_coord}
    region_frontier = {start_coord}

    steps_taken = 0
    while len(region_frontier) != 0:
        steps_taken += 1
        new_frontier = set()
        for coord in region_frontier:
            for i, j in [(coord[0] - 1, coord[1]),
                         (coord[0] + 1, coord[1]),
                         (coord[0], coord[1] - 1),
                         (coord[0], coord[1] + 1)]:
                neighbour_coord = (i, j)
                if neighbour_coord in region_coords or neighbour_coord in blocks:
                    continue

                if neighbour_coord == end_coord:
                    return steps_taken

                if 0 <= i < board_size and 0 <= j < board_size:
                    new_frontier.add(neighbour_coord)
                    region_coords.add(neighbour_coord)

        region_frontier = new_frontier

    return None


def find_min_path_length(filename_str: str, board_size: int, num_blocks_fallen: int) -> int:
    content = load_file(filename_str)

    falling_blocks = [tuple(int(i) for i in l.split(','))for l in content]

    return compute_path_len(set(falling_blocks[:num_blocks_fallen]), board_size)


if __name__ == "__main__":

    test_res = find_min_path_length("data1_test.txt", 7, 12)
    assert test_res == 22
    start = time()
    print(find_min_path_length("data1_real.txt", 71, 1024))
    print("Execution time:", time() - start)
