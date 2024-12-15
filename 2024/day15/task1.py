from time import time
from typing import Optional

from utils.file_utils import load_file, chunk_input

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

MOVEMENT = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1)
}


def check_step(warehouse_map: list[list[str]], coord: tuple[int, int], direction: str) \
        -> tuple[bool, Optional[tuple[int, int]], Optional[tuple[int, int]]]:

    i, j = coord
    d_i = MOVEMENT[direction][0]
    d_j = MOVEMENT[direction][1]
    i += d_i
    j += d_j

    robot_to = (i, j)
    bumped_box = False
    while warehouse_map[i][j] != '.':
        assert i >= 0 and j >= 0 and i < len(
            warehouse_map) and j < len(warehouse_map[0])
        if warehouse_map[i][j] == '#':
            return False, None, None
        if warehouse_map[i][j] == 'O':
            bumped_box = True

        i += d_i
        j += d_j

    return True, robot_to, (i, j) if bumped_box else None


def sum_box_coords(filename_str: str) -> int:

    content = load_file(filename_str)

    warehouse_map, command_inputs = chunk_input(content, "")

    robot_coord = None
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '@':
                robot_coord = (i, j)
                break

        if robot_coord:
            break

    warehouse_map = [list(row) for row in warehouse_map]

    for cs in command_inputs:
        for c in cs:
            valid_step, robot_to, box_to = check_step(
                warehouse_map, robot_coord, c)

            if valid_step:
                warehouse_map[robot_coord[0]][robot_coord[1]] = '.'
                warehouse_map[robot_to[0]][robot_to[1]] = '@'
                assert robot_to is not None
                robot_coord = robot_to
                if box_to is not None:
                    warehouse_map[box_to[0]][box_to[1]] = 'O'

    coord_sum = 0
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == 'O':
                coord_sum += 100 * i + j

    return coord_sum


if __name__ == "__main__":

    test_small_res = sum_box_coords("data1_test_small.txt")
    assert test_small_res == 2028, f"Test failed: {test_small_res}"

    test_res = sum_box_coords("data1_test.txt")
    assert test_res == 10092, f"Test failed: {test_res}"
    start = time()
    print(sum_box_coords("data1_real.txt"))
    print("Execution time:", time() - start)
