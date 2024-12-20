import heapq
from time import time

from utils.file_utils import load_file


def compute_distance_map(track_map: list[str], end_coord: tuple[int, int]) -> dict[tuple[int, int], int]:
    """
    Computes the distance from every coordinate to the end coordinate
    """

    num_rows = len(track_map)
    num_cols = len(track_map[0])

    distance_map = {end_coord: 0}

    frontier = {end_coord}

    steps_taken = 0
    while len(frontier) != 0:
        steps_taken += 1
        new_frontier = set()
        for coord in frontier:
            for i, j in [(coord[0] - 1, coord[1]),
                         (coord[0] + 1, coord[1]),
                         (coord[0], coord[1] - 1),
                         (coord[0], coord[1] + 1)]:

                neighbour_coord = (i, j)
                if not (0 <= i < num_rows and 0 <= j < num_cols):
                    continue

                if neighbour_coord in distance_map or track_map[i][j] == '#':
                    continue

                new_frontier.add(neighbour_coord)
                distance_map[neighbour_coord] = steps_taken

        frontier = new_frontier

    return distance_map


def find_best_skip(filename_str: str, max_skip: int) -> tuple[dict[int, int]]:

    content = load_file(filename_str)

    start_coord = None
    end_coord = None
    for i, row in enumerate(content):
        for j, cell in enumerate(row):
            if cell == 'S':
                start_coord = (i, j)

            if cell == 'E':
                end_coord = (i, j)

            if start_coord and end_coord:
                break

        if start_coord and end_coord:
            break

    assert start_coord and end_coord

    distance_map = compute_distance_map(content, end_coord)

    skips = {}
    for skip_start, skip_start_dist in distance_map.items():
        i, j = skip_start
        for d_i in range(-max_skip, max_skip + 1):
            abs_d_i = abs(d_i)
            for d_j in range(-max_skip + abs_d_i, max_skip - abs_d_i + 1):
                skip_end = (i + d_i, j + d_j)
                if skip_end in distance_map:
                    skipped = skip_start_dist - \
                        distance_map[skip_end] - abs_d_i - abs(d_j)
                    if skipped > 0:
                        if skipped not in skips:
                            skips[skipped] = []
                        skips[skipped].append((skip_start, skip_end))

    return {k: len(v) for k, v in skips.items()}


if __name__ == "__main__":
    print("Task 1")
    test_res = find_best_skip("data1_test.txt", 2)
    test_expected = {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    assert test_res == test_expected, f"Test failed: {test_res}"

    start = time()
    print(sum(v for k, v in find_best_skip(
        "data1_real.txt", 2).items() if k >= 100))
    print("Execution time:", time() - start)

    print("Task 2")
    test_res_2 = find_best_skip("data1_test.txt", 20)

    expected_ge_50 = {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
    test_res_ge_50 = {k: v for k, v in test_res_2.items() if k >= 50}
    assert test_res_ge_50 == expected_ge_50, f"Test failed: {test_res_ge_50}"

    start = time()
    print(sum(v for k, v in find_best_skip(
        "data1_real.txt", 20).items() if k >= 100))
    print("Execution time:", time() - start)
