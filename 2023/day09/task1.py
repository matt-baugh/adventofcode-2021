import math
from pathlib import Path

from utils.file_utils import parse_file_lines


def sum_preds(filename: str):
    file_lines = parse_file_lines(Path(__file__).parent / filename)

    pred_sum = 0
    for line in file_lines:
        nums = [int(n) for n in line]
        levels = [nums]
        while not all(n == 0 for n in levels[-1]):
            levels.append([a - b for a, b in zip(levels[-1][1:], levels[-1])])

        # print('num_levels', len(levels))
        # print('levels', levels)

        for i in range(len(levels) - 1)[::-1]:
            levels[i].append(levels[i][-1] + levels[i + 1][-1])

        # print('pred', levels[0][-1])

        pred_sum += levels[0][-1]

    return pred_sum


if __name__ == "__main__":
    test_sol = sum_preds("data1_test.txt")
    print(test_sol)
    assert test_sol == 114
    print(sum_preds("data1_real.txt"))
