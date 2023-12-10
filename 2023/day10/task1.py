import math
from pathlib import Path

from utils.file_utils import load_file, split_str

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
PIPES = {
    '|': (NORTH, 2),
    '-': (1, 3),
    'L': (NORTH, 1),
    'J': (NORTH, 3),
    '7': (2, 3),
    'F': (1, 2)
}
MOVEMENTS = {
    NORTH: lambda y, x: (y - 1, x),
    EAST: lambda y, x: (y, x + 1),
    SOUTH: lambda y, x: (y + 1, x),
    WEST: lambda y, x: (y, x - 1)
}


GROUND = '.'
START = 'S'


def find_furthest_point(filename: str):
    file_lines = load_file(Path(__file__).parent / filename)
    pipe_map = [[c for c in line] for line in file_lines]

    # Find starting point:

    start_row = [i for i, r in enumerate(pipe_map) if START in r][0]
    start_col = pipe_map[start_row].index(START)
    start_pos = (start_row, start_col)

    pos_and_from = []
    for pos, to_dir in [(MOVEMENTS[d](*start_pos), d) for d in (NORTH, EAST, SOUTH, WEST)]:
        pos_char = pipe_map[pos[0]][pos[1]]
        from_dir = (to_dir + 2) % 4
        if pos_char != GROUND:
            if from_dir in PIPES[pos_char]:
                pos_and_from.append((pos, from_dir))

    assert len(pos_and_from) == 2, (pos_and_from, pipe_map[start_row - 1: start_row + 2])
    steps = 1

    while pos_and_from[0][0] != pos_and_from[1][0]:
        # print(pos_and_from)
        new_pos_and_from = []

        for p, f in pos_and_from:
            p_char = pipe_map[p[0]][p[1]]
            p_char_dirs = PIPES[p_char]
            p_to_dir = [d for d in p_char_dirs if d != f][0]

            new_p = MOVEMENTS[p_to_dir](*p)
            new_f = (p_to_dir + 2) % 4
            new_pos_and_from.append((new_p, new_f))

        pos_and_from = new_pos_and_from
        steps += 1

    return steps


if __name__ == "__main__":
    test_sol = find_furthest_point("data1_test.txt")
    print(test_sol)
    assert test_sol == 4
    test_sol = find_furthest_point("data1_test_5.txt")
    print(test_sol)
    assert test_sol == 4
    test_sol2 = find_furthest_point("data1_test2.txt")
    print(test_sol2)
    assert test_sol2 == 8
    test_sol2 = find_furthest_point("data1_test2_5.txt")
    print(test_sol2)
    assert test_sol2 == 8
    print(find_furthest_point("data1_real.txt"))
