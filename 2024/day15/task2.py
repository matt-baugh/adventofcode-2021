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


def check_step_h(warehouse_map: list[list[str]], coord: tuple[int, int], direction: str) \
        -> tuple[bool, Optional[tuple[int, int]], Optional[tuple[int, int]]]:

    i, j = coord
    d_i = MOVEMENT[direction][0]
    d_j = MOVEMENT[direction][1]
    i += d_i
    j += d_j

    while warehouse_map[i][j] != '.':
        assert i >= 0 and j >= 0 and i < len(
            warehouse_map) and j < len(warehouse_map[0])

        if warehouse_map[i][j] == '#':
            return False, None

        i += d_i
        j += d_j

    return True, (i, j)


def render_map(warehouse_map: list[list[str]]):
    print("-" * len(warehouse_map[0]))
    for row in warehouse_map:
        print("".join(row))
    print("-" * len(warehouse_map[0]))


def check_step_v(warehouse_map: list[list[str]], coord: tuple[int, int], direction: str) \
        -> bool:

    i, j = coord
    d_i = MOVEMENT[direction][0]
    d_j = MOVEMENT[direction][1]
    i += d_i
    j += d_j

    while warehouse_map[i][j] != '.':
        assert i >= 0 and j >= 0 and i < len(
            warehouse_map) and j < len(warehouse_map[0])

        if warehouse_map[i][j] == '#':
            return False

        if warehouse_map[i][j] == '[':
            if warehouse_map[i][j + 1] != ']':
                render_map(warehouse_map)
                raise ValueError(f"Box broken! {warehouse_map[i][j + 1]}")
            return check_step_v(warehouse_map, (i, j), direction) and check_step_v(warehouse_map, (i, j + 1), direction)

        if warehouse_map[i][j] == ']':
            if warehouse_map[i][j - 1] != '[':
                render_map(warehouse_map)
                raise ValueError(f"Box broken! {warehouse_map[i][j - 1]}")
            return check_step_v(warehouse_map, (i, j), direction) and check_step_v(warehouse_map, (i, j - 1), direction)

        i += d_i
        j += d_j

    return True


def step_v(warehouse_map: list[list[str]], coord: tuple[int, int], direction: str, last_cell: str):

    i, j = coord
    d_i = MOVEMENT[direction][0]
    d_j = MOVEMENT[direction][1]

    tmp_cell = last_cell
    last_cell = warehouse_map[i][j]
    warehouse_map[i][j] = tmp_cell

    i += d_i
    j += d_j

    if warehouse_map[i][j] == '.':
        warehouse_map[i][j] = last_cell
        return
    elif warehouse_map[i][j] == '#':
        render_map(warehouse_map)
        raise ValueError(f"Step approved yet found box at {
                         i}, {j}: {warehouse_map[i][j]}")
    elif warehouse_map[i][j] == '[':
        if warehouse_map[i][j + 1] != ']':
            render_map(warehouse_map)
            raise ValueError(f"Box broken! {warehouse_map[i][j + 1]}")

        step_v(warehouse_map, (i, j), direction, last_cell=last_cell)
        step_v(warehouse_map, (i, j + 1), direction, last_cell='.')

    elif warehouse_map[i][j] == ']':
        if warehouse_map[i][j - 1] != '[':
            render_map(warehouse_map)
            raise ValueError(f"Box broken! {warehouse_map[i][j - 1]}")

        step_v(warehouse_map, (i, j), direction, last_cell=last_cell)
        step_v(warehouse_map, (i, j - 1), direction, last_cell='.')
    else:
        render_map(warehouse_map)
        raise ValueError(f"Invalid cell: {warehouse_map[i][j]}")


def expand(cell: str):
    if cell == '#':
        return '##'
    elif cell == '.':
        return '..'
    elif cell == 'O':
        return '[]'
    elif cell == '@':
        return '@.'
    else:
        raise ValueError(f"Invalid cell: {cell}")


def is_horizontal(direction: str) -> bool:
    return direction in [LEFT, RIGHT]


def sum_box_coords(filename_str: str) -> int:

    content = load_file(filename_str)

    warehouse_map, command_inputs = chunk_input(content, "")

    warehouse_map = [[c for cell in row for c in expand(cell)]
                     for row in warehouse_map]

    robot_coord = None
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '@':
                robot_coord = (i, j)
                break

        if robot_coord:
            break

    for cs in command_inputs:
        for c in cs:

            if is_horizontal(c):
                valid_step, cell_into = check_step_h(
                    warehouse_map, robot_coord, c)

                if valid_step:
                    assert cell_into[0] == robot_coord[0], \
                        f"Invalid move: {c}, {robot_coord} -> {cell_into}"
                    curr_row = warehouse_map[robot_coord[0]]
                    if c == RIGHT:
                        curr_row[robot_coord[1] + 1: cell_into[1] +
                                 1] = curr_row[robot_coord[1]: cell_into[1]]
                    else:
                        assert c == LEFT, f"Invalid direction: {c}"
                        curr_row[cell_into[1]: robot_coord[1]
                                 ] = curr_row[cell_into[1] + 1: robot_coord[1] + 1]

                    curr_row[robot_coord[1]] = '.'
                    robot_coord = tuple(
                        i + d for i, d in zip(robot_coord, MOVEMENT[c]))

            else:
                if check_step_v(warehouse_map, robot_coord, c):
                    step_v(warehouse_map, robot_coord, c, last_cell='.')
                    robot_coord = tuple(
                        i + d for i, d in zip(robot_coord, MOVEMENT[c]))

    coord_sum = 0
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '[':
                coord_sum += 100 * i + j

    return coord_sum


if __name__ == "__main__":

    test_res = sum_box_coords("data1_test.txt")
    assert test_res == 9021, f"Test failed: {test_res}"
    start = time()
    print(sum_box_coords("data1_real.txt"))
    print("Execution time:", time() - start)
