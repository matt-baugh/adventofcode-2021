from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation

from utils.file_utils import load_file

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


def find_enclosed_area(filename: str):
    file_lines = load_file(Path(__file__).parent / filename)
    pipe_map = [[c for c in line] for line in file_lines]
    
    def pos_in_map(pos):
        return 0 <= pos[0] < len(pipe_map) and 0 <= pos[1] < len(pipe_map[pos[0]])

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

    assert len(pos_and_from) == 2, (pos_and_from,
                                    pipe_map[start_row - 1: start_row + 2])

    loop_map = np.array([[False for _ in range(len(r))] for r in pipe_map])
    loop_map[start_pos] = True
    init_pos_and_from = pos_and_from.copy()

    while pos_and_from[0][0] != pos_and_from[1][0]:

        loop_map[pos_and_from[0][0]] = True
        loop_map[pos_and_from[1][0]] = True

        new_pos_and_from = []

        for pos_i, (p, f) in enumerate(pos_and_from):

            # pipe following
            p_char = pipe_map[p[0]][p[1]]
            p_char_dirs = PIPES[p_char]
            p_to_dir = [d for d in p_char_dirs if d != f][0]

            new_p = MOVEMENTS[p_to_dir](*p)
            new_f = (p_to_dir + 2) % 4
            new_pos_and_from.append((new_p, new_f))

        pos_and_from = new_pos_and_from

    # Do final end of loop:
    loop_map[pos_and_from[0][0]] = True
    
    
    enclosed_map_pos = np.array(
        [[False for _ in range(len(r))] for r in pipe_map])
    enclosed_map_neg = np.array(
        [[False for _ in range(len(r))] for r in pipe_map])

    pos_orientations = [+1, -1]
    pos_and_from = init_pos_and_from
    
    def update_maps(curr_in_dir, curr_pos):
        # area marking
        curr_inward_pos = MOVEMENTS[curr_in_dir](*curr_pos)
        if pos_in_map(curr_inward_pos) and not loop_map[curr_inward_pos[0]][curr_inward_pos[1]]:
            enclosed_map_pos[curr_inward_pos] = True
        
        curr_outward_pos = MOVEMENTS[(curr_in_dir + 2) % 4](*curr_pos)
        if pos_in_map(curr_outward_pos) and not loop_map[curr_outward_pos[0]][curr_outward_pos[1]]:
            enclosed_map_neg[curr_outward_pos] = True
    
    for pos_i, (_, f) in enumerate(pos_and_from):
        # init_dir = (f + 2) % 4
        update_maps((f + pos_orientations[pos_i]) % 4, start_pos)
    
    while pos_and_from[0][0] != pos_and_from[1][0]:

        loop_map[pos_and_from[0][0]] = True
        loop_map[pos_and_from[1][0]] = True

        new_pos_and_from = []

        for pos_i, (p, f) in enumerate(pos_and_from):

            update_maps((f + pos_orientations[pos_i]) % 4, p)

            # pipe following
            p_char = pipe_map[p[0]][p[1]]
            p_char_dirs = PIPES[p_char]
            p_to_dir = [d for d in p_char_dirs if d != f][0]
            update_maps((p_to_dir + -1 * pos_orientations[pos_i]) % 4, p)

            new_p = MOVEMENTS[p_to_dir](*p)
            new_f = (p_to_dir + 2) % 4
            new_pos_and_from.append((new_p, new_f))

        pos_and_from = new_pos_and_from

    for pos_i, (p, f) in enumerate(pos_and_from):
        update_maps((f + pos_orientations[pos_i]) % 4, p)

    assert not np.any(enclosed_map_pos & enclosed_map_neg)

    no_loop = np.logical_not(loop_map)
    enclosed_map_pos = binary_dilation(enclosed_map_pos, iterations=-1, mask=no_loop)
    enclosed_map_neg = binary_dilation(enclosed_map_neg, iterations=-1, mask=no_loop)
    assert not np.any(enclosed_map_pos & enclosed_map_neg)
    print('Pos sum filled', np.sum(enclosed_map_pos))
    print('Neg sum filled', np.sum(enclosed_map_neg))

    return min(np.sum(enclosed_map_pos), np.sum(enclosed_map_neg))


if __name__ == "__main__":
    test_sol = find_enclosed_area("data2_test.txt")
    assert test_sol == 4
    test_sol2 = find_enclosed_area("data2_test2.txt")
    assert test_sol2 == 8
    test_sol3 = find_enclosed_area("data2_test3.txt")
    assert test_sol3 == 10
    print(find_enclosed_area("data1_real.txt"))
