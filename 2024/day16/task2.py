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


def min_dist_to(coord: tuple[int, int], min_to: dict) -> int:
    min_dist = float('inf')
    for d in DIRECTIONS:
        if (coord, d) in min_to and min_to[(coord, d)][0] < min_dist:
            min_dist = min_to[(coord, d)][0]
    return min_dist


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

    boundary = [(0, ((start_coord, EAST), None))]
    visited = set()
    min_to = {}

    found_path = False
    while len(boundary) > 0:
        dist, (pos, pos_from) = heapq.heappop(boundary)

        if pos in visited:
            assert pos in min_to
            if min_to[pos][0] == dist:
                min_to[pos][1].append(pos_from)
            continue

        if found_path and dist > min_dist_to(end_coord, min_to):
            break

        coord, direction = pos

        visited.add(pos)
        min_to[pos] = [dist, [pos_from] if pos_from is not None else []]

        if coord == end_coord:
            found_path = True
            continue

        l_dir = rotate_left(direction)
        heapq.heappush(boundary, (dist + ROTATE_COST, ((coord, l_dir), pos)))

        r_dir = rotate_right(direction)
        heapq.heappush(boundary, (dist + ROTATE_COST, ((coord, r_dir), pos)))

        ahead_c = step(coord, direction)
        steps_taken = 1
        if content[ahead_c[0]][ahead_c[1]] != '#':
            heapq.heappush(boundary, (dist + MOVE_COST *
                                      steps_taken, ((ahead_c, direction), pos)))

    min_dist = min_dist_to(end_coord, min_to)
    on_path = set()
    walk_back = [(end_coord, d) for d in DIRECTIONS if (end_coord, d)
                 in min_to and min_to[(end_coord, d)][0] == min_dist]
    while len(walk_back) > 0:
        new_walk_back = []
        for p in walk_back:
            on_path.add(p[0])
            new_walk_back.extend(min_to[p][1])

        walk_back = new_walk_back

    return len(on_path)


if __name__ == "__main__":

    test_res = find_shortest_path("data1_test1.txt")
    assert test_res == 45, f"Test failed: {test_res}"

    test_res = find_shortest_path("data1_test2.txt")
    assert test_res == 64, f"Test failed: {test_res}"

    start = time()
    print(find_shortest_path("data1_real.txt"))
    print("Execution time:", time() - start)
