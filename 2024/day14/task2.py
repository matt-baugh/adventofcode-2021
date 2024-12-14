import re
from time import time

from utils.file_utils import load_file


def render(positions: list[int], num_rows: int, num_cols: int) -> None:

    grid = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]

    for pos in positions:
        grid[pos[0]][pos[1]] = '#'

    print('-' * num_cols)
    for row in grid:
        print(''.join(row))
    print('-' * num_cols)


def compute_variances(ps: list[list[int]]) -> float:
    ps_ys, ps_xs = zip(*ps)
    mean_y = sum(ps_ys) / len(ps)
    mean_x = sum(ps_xs) / len(ps)
    var_y = sum((y - mean_y) ** 2 for y in ps_ys) / len(ps)
    var_x = sum((x - mean_x) ** 2 for x in ps_xs) / len(ps)
    return var_y, var_x


def mul_safety_scores(filename_str: str, num_rows: int, num_cols: int, num_steps: int) -> int:

    content = load_file(filename_str)

    ps = []
    vs = []
    for l in content:
        pos_x, pos_y, v_x, v_y = map(int, re.findall(r"-?\d+", l))
        ps.append([pos_y, pos_x])
        vs.append([v_y, v_x])

    min_x_var = float('inf')
    min_y_var = float('inf')
    min_var_step = -1

    for i in range(num_steps):
        y_var, x_var = compute_variances(ps)
        if x_var < min_x_var and y_var < min_y_var:
            min_x_var = x_var
            min_y_var = y_var
            min_var_step = i
            print(f"Step: {i}, x_var: {x_var}, y_var: {y_var}")

            render(ps, num_rows, num_cols)

        ps = [((p_y + vs[j][0]) % num_rows, (p_x + vs[j][1]) % num_cols)
              for j, (p_y, p_x) in enumerate(ps)]

    return min_var_step


if __name__ == "__main__":

    start = time()
    print(mul_safety_scores("data1_real.txt",
          num_rows=103, num_cols=101, num_steps=10000))
    print("Execution time:", time() - start)
