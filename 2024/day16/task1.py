import heapq
from time import time

from utils.file_utils import load_file


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
DIR_MOV = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1)
}

ROTATE_COST = 1000
MOVE_COST = 1


def rotate_left(direction: int) -> int:
    return (direction - 1) % 4


def rotate_right(direction: int) -> int:
    return (direction + 1) % 4


def step(coord: tuple[int, int], direction: int) -> tuple[int, int]:
    return coord[0] + DIR_MOV[direction][0], coord[1] + DIR_MOV[direction][1]


def find_shortest_path(filename_str: str) -> int:

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

    boundary = [(0, (start_coord, EAST))]
    visited = set()

    while len(boundary) > 0:
        dist, pos = heapq.heappop(boundary)

        if pos in visited:
            continue

        coord, direction = pos

        if coord == end_coord:
            return dist

        visited.add(pos)

        l_dir = rotate_left(direction)
        if (coord, l_dir) not in visited:
            heapq.heappush(boundary, (dist + ROTATE_COST, (coord, l_dir)))

        r_dir = rotate_right(direction)
        if (coord, r_dir) not in visited:
            heapq.heappush(boundary, (dist + ROTATE_COST, (coord, r_dir)))

        ahead_c = step(coord, direction)
        steps_taken = 1
        while content[ahead_c[0]][ahead_c[1]] != '#':
            if (ahead_c, direction) not in visited:
                heapq.heappush(boundary, (dist + MOVE_COST *
                               steps_taken, (ahead_c, direction)))
            else:
                break
            steps_taken += 1
            ahead_c = step(ahead_c, direction)


if __name__ == "__main__":

    test_res = find_shortest_path("data1_test1.txt")
    assert test_res == 7036, f"Test failed: {test_res}"

    test_res = find_shortest_path("data1_test2.txt")
    assert test_res == 11048, f"Test failed: {test_res}"

    start = time()
    print(find_shortest_path("data1_real.txt"))
    print("Execution time:", time() - start)
