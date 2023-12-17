from pathlib import Path

from day16.task1 import calc_energy_from, MIRROR_CHARS, NORTH, SOUTH, EAST, WEST
import day16
from utils.file_utils import load_file

PRINT = False
day16.task1.PRINT = False


def calc_max_energy(filename: str) -> int:
    raw_input = load_file(Path(__file__).parent / filename)

    all_mirrors = []
    for i, r in enumerate(raw_input):
        for j, c in enumerate(r):
            if c in MIRROR_CHARS:
                all_mirrors.append(((i, j), c))

    input_shape = (len(raw_input), len(raw_input[0]))

    max_energy = 0
    for i in range(input_shape[0]):
        for b in [((i, 0), EAST), ((i, input_shape[1] - 1), WEST)]: 
            new_e = calc_energy_from(b, all_mirrors, input_shape)
            if new_e > max_energy:
                max_energy = new_e
                if PRINT:
                    print("New max energy:", max_energy, b)

    for j in range(input_shape[1]):
        for b in [((0, j), SOUTH), ((input_shape[0] - 1, j), NORTH)]:
            new_e = calc_energy_from(b, all_mirrors, input_shape)
            if new_e > max_energy:
                max_energy = new_e
                if PRINT:
                    print("New max energy:", max_energy, b)

    return max_energy


if __name__ == "__main__":
    test_sol = calc_max_energy("data1_test.txt")
    print(test_sol)
    assert test_sol == 51
    real_sol = calc_max_energy("data1_real.txt")
    print(real_sol)
    # assert real_sol == 513643
