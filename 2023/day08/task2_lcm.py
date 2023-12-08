import math
from pathlib import Path

from utils.file_utils import load_file


def steps_to_reach(filename: str):
    file_lines = load_file(Path(__file__).parent / filename)

    path_instructions = file_lines[0]

    path_map = {}

    for l in file_lines[2:]:
        ws = l.split()
        # print(ws)
        path_map[ws[0]] = (ws[2][1:-1], ws[3][:-1])

    locs = [l for l in path_map.keys() if l[-1] == "A"]
    step = 0

    looping_locs_cache = {}
    print('Num possible locs:', len(path_map.keys()))

    end_steps = []

    for loc in locs:

        step = 0
        interim_loc = loc
        while interim_loc[-1] != "Z":
            direction = path_instructions[step % len(path_instructions)]

            interim_loc = path_map[interim_loc][0] if direction == "L" else path_map[interim_loc][1]

            step += 1

        end_steps.append(step)
        
    print(end_steps)

    return math.lcm(*end_steps)


if __name__ == "__main__":
    test_sol = steps_to_reach("data1_test.txt")
    print(test_sol)
    assert test_sol == 6
    test_sol2 = steps_to_reach("data1_test2.txt")
    print(test_sol2)
    assert test_sol2 == 2
    test_sol3 = steps_to_reach("data2_test.txt")
    assert test_sol3 == 6
    print(test_sol3)
    print(steps_to_reach("data1_real.txt"))
