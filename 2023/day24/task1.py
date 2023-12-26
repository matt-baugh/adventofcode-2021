from pathlib import Path

import numpy as np

from utils.file_utils import parse_file_lines

PRINT = False


def calc_num_intersections(filename: str, min_coord: int, max_coord: int, num_dims: int) -> int:
    raw_input = parse_file_lines(
        Path(__file__).parent / filename, ('@', (',', ',')), skip_empty=True)

    hailstone_paths = [tuple(np.array(list(map(int, v)))
                             for v in p) for p in raw_input]

    num_intersects = 0
    for i, (s1_coord, s1_vel) in enumerate(hailstone_paths):
        s1_coord = s1_coord[:num_dims]
        s1_vel = s1_vel[:num_dims]
        for s2_coord, s2_vel in hailstone_paths[i + 1:]:
            s2_coord = s2_coord[:num_dims]
            s2_vel = s2_vel[:num_dims]

            # s1_x + s1_vx * t_1 = s2_x + s2_vx * t_2
            # s1_y + s1_vy * t_1 = s2_y + s2_vy * t_2
            # ->
            # t_1 = (s2_x - s1_x + s2_vx * t_2) / s1_vx
            # t_1 = (s2_y - s1_y + s2_vy * t_2) / s1_vy
            # ->
            # d_x = s2_x - s1_x, d_y = s2_y - s1_y
            # t_1 = (d_x + s2_vx * t_2) / s1_vx
            # t_1 = (d_y + s2_vy * t_2) / s1_vy
            # ->
            # (d_x + s2_vx * t_2) / s1_vx = (d_y + s2_vy * t_2) / s1_vy
            # ->
            # d_x * s1_vy + s2_vx * s1_vy * t_2 = d_y * s1_vx + s2_vy * s1_vx * t_2
            # ->
            # d_x * s1_vy - d_y * s1_vx = t_2 * (s2_vy * s1_vx - s2_vx * s1_vy)
            # ->
            # t_2 = (d_x * s1_vy - d_y * s1_vx) / (s2_vy * s1_vx - s2_vx * s1_vy)
            diff = s2_coord - s1_coord
            t_2 = (diff[0] * s1_vel[1] - diff[1] * s1_vel[0]) / \
                (s2_vel[1] * s1_vel[0] - s2_vel[0] * s1_vel[1])
            intersect = s2_coord + s2_vel * t_2
            if t_2 < 0:
                continue
            t_1 = (intersect - s1_coord) / s1_vel
            assert np.allclose(t_1[0], t_1[1:]), 't_1: ' + str(t_1)
            if t_1[0] < 0:
                continue
            if all(min_coord <= c <= max_coord for c in intersect):
                if PRINT:
                    print(s1_coord, s1_vel, s2_coord, s2_vel, intersect)
                num_intersects += 1

    return num_intersects


if __name__ == "__main__":
    test_sol = calc_num_intersections("data1_test.txt", 7, 27, 2)
    print(test_sol)
    assert test_sol == 2
    real_sol = calc_num_intersections(
        "data1_real.txt", 200000000000000, 400000000000000, 2)
    print(real_sol)
    assert real_sol == 24192
