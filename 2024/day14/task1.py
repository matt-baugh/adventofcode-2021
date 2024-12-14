import re
from time import time

from utils.file_utils import load_file


def mul_safety_scores(filename_str: str, num_rows: int, num_cols: int, num_steps: int) -> int:

    content = load_file(filename_str)

    print(f"Num robots: {len(content)}")

    safety_scores = [[0, 0], [0, 0]]

    mid_x = num_cols // 2
    mid_y = num_rows // 2

    for l in content:
        pos_x, pos_y, v_x, v_y = map(int, re.findall(r"-?\d+", l))

        x = (pos_x + v_x * num_steps) % num_cols
        y = (pos_y + v_y * num_steps) % num_rows

        if x == mid_x or y == mid_y:
            continue

        quad_x = int(x > mid_x)
        quad_y = int(y > mid_y)
        safety_scores[quad_y][quad_x] += 1

    return safety_scores[0][0] * safety_scores[0][1] * safety_scores[1][0] * safety_scores[1][1]


if __name__ == "__main__":

    test_res = mul_safety_scores(
        "data1_test.txt", num_rows=7, num_cols=11, num_steps=100)
    assert test_res == 12, f"Test failed: {test_res}"
    start = time()
    print(mul_safety_scores("data1_real.txt",
          num_rows=103, num_cols=101, num_steps=100))
    print("Execution time:", time() - start)
