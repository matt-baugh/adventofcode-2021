from pathlib import Path

from tqdm import tqdm

from utils.file_utils import load_file

PRINT = False

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

DIR_AXIS = {
    NORTH: 0,
    WEST: 1,
    SOUTH: 0,
    EAST: 1
}

ORDER_AXIS = {
    NORTH: False,
    WEST: False,
    SOUTH: True,
    EAST: True
}


def group_by_axis(rocks: list[tuple[int, int]], axis: int, sort_descending: bool) -> dict[int, list[tuple[int, int]]]:
    grouped = {}
    for r in rocks:
        grouped[r[axis]] = grouped.get(r[axis], []) + [r]

    # N - Inc
    # W - Inc
    # S - Inc, E

    assert True
    return {k: v[::-1] if sort_descending else v for k, v in grouped.items()}


def tilt_rocks(round_rocks: list[tuple[int, int]], cube_rocks: list[tuple[int, int]], tilt_dir: int, num_rows: int,
               num_cols: int) \
        -> list[tuple[int, int]]:

    dir_axis = DIR_AXIS[tilt_dir]
    # Group by other axis
    group_axis = 1 - dir_axis
    tilt_upwards = ORDER_AXIS[tilt_dir]
    round_rocks = group_by_axis(
        round_rocks, group_axis, sort_descending=tilt_upwards)
    cube_rocks = group_by_axis(
        cube_rocks, group_axis, sort_descending=tilt_upwards)

    new_round_rocks = []
    start_pos = [num_rows - 1, num_cols - 1][dir_axis] if tilt_upwards else 0

    for k, r_rocks in sorted(round_rocks.items()):
        c_rocks = cube_rocks.get(k, [])
        next_rock_pos = start_pos
        for r in r_rocks:
            while len(c_rocks) != 0 and (r[dir_axis] > c_rocks[0][dir_axis]) ^ tilt_upwards:
                next_rock_pos = c_rocks[0][dir_axis] + \
                    (-1 if tilt_upwards else 1)
                c_rocks = c_rocks[1:]

            new_round_rocks.append(
                tuple((k if d == group_axis else next_rock_pos)for d in range(2)))
            next_rock_pos += (-1 if tilt_upwards else 1)

    return new_round_rocks


def gen_rock_grid(round_rocks: list[tuple[int, int]], cube_rocks: list[tuple[int, int]], num_rows: int, num_cols: int) \
        -> str:
    rock_grid = [['.' for _ in range(num_cols)] for _ in range(num_rows)]
    for r in round_rocks:
        rock_grid[r[0]][r[1]] = 'O'
    for r in cube_rocks:
        rock_grid[r[0]][r[1]] = '#'

    return '\n'.join([''.join(row) for row in rock_grid])


def calc_north_load(filename: str, cycles: int) -> int:
    all_input = load_file(Path(__file__).parent / filename)

    num_rows = len(all_input)
    num_cols = len(all_input[0])

    cube_rocks = []
    round_rocks = []

    # Parse input into sparse representation
    for row_i, row in enumerate(all_input):
        for col_i, c in enumerate(row):
            if c == '.':
                continue
            elif c == '#':
                cube_rocks.append((row_i, col_i))
            else:
                assert c == 'O'
                round_rocks.append((row_i, col_i))

    # round_rocks are ordered by row_i, col_i
    # cube_rocks are ordered by row_i, col_i

    rock_record = {}
    map_record = {}
    for c in tqdm(range(cycles)):

        for d in range(4):
            round_rocks = tilt_rocks(
                round_rocks, cube_rocks, d, num_rows, num_cols)
        
        rock_map = gen_rock_grid(round_rocks, cube_rocks, num_rows, num_cols)
        
        if PRINT and c < 3:
            print()
            print(rock_map)
            print()
            
        if rock_map in rock_record:
            print(f"Found cycle at {c}! (prev {rock_record[rock_map]}))")
            break
        else:
            rock_record[rock_map] = c
            map_record[c] = round_rocks

    cycle_start = rock_record[rock_map]
    cycle_end = c
    cycle_len = cycle_end - cycle_start
    round_rocks = map_record[cycle_start + ((cycles - 1) - cycle_start) % cycle_len]

    total = sum([num_rows - c_i for c_i, _ in round_rocks])

    return total


if __name__ == "__main__":
    test_sol = calc_north_load("data1_test.txt", 1000000000)
    print(test_sol)
    assert test_sol == 64
    real_sol = calc_north_load("data1_real.txt", 1000000000)
    print(real_sol)
    assert real_sol == 96105
