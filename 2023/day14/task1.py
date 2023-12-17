from pathlib import Path

from utils.file_utils import load_file

PRINT = False


def calc_north_load(filename: str) -> int:
    all_input = load_file(Path(__file__).parent / filename)

    max_load = len(all_input)

    total = 0
    for col_i in range(len(all_input[0])):
        curr_cube = -1
        cube_dict = {
            curr_cube: []
        }
        for row_i, row in enumerate(all_input):
            c = row[col_i]
            if c == '.':
                continue

            if c == '#':
                curr_cube = row_i
                cube_dict[curr_cube] = []

            if c == 'O':
                cube_dict[curr_cube].append(row_i)

        total += sum(sum((max_load - (c + 1 + r)) for r in range(len(rocks)))
                     for c, rocks in cube_dict.items())

    return total


if __name__ == "__main__":
    test_sol = calc_north_load("data1_test.txt")
    print(test_sol)
    assert test_sol == 136
    real_sol = calc_north_load("data1_real.txt")
    print(real_sol)
    # assert real_sol == 6935
