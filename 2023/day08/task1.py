import math
from pathlib import Path

from utils.file_utils import load_file, split_str


def steps_to_reach(filename: str):
    file_lines = load_file(Path(__file__).parent / filename)

    path_instructions = file_lines[0]

    path_map = {}

    for l in file_lines[2:]:
        ws = l.split()
        # print(ws)
        path_map[ws[0]] = (ws[2][1:-1], ws[3][:-1])

    loc = "AAA"
    step = 0

    while loc != "ZZZ":
        direction = path_instructions[step % len(path_instructions)]

        if direction == "L":
            loc = path_map[loc][0]
        else:
            assert direction == "R"
            loc = path_map[loc][1]

        step += 1

    return step


if __name__ == "__main__":
    test_sol = steps_to_reach("data1_test.txt")
    print(test_sol)
    assert test_sol == 6
    test_sol2 = steps_to_reach("data1_test2.txt")
    print(test_sol2)
    assert test_sol2 == 2
    print(steps_to_reach("data1_real.txt"))
