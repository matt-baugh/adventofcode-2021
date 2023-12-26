from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from utils.file_utils import parse_file_lines

PRINT = False


def calc_throw_pos(filename: str, min_coord: int, max_coord: int, num_dims: int) -> int:
    raw_input = parse_file_lines(
        Path(__file__).parent / filename, ('@', (',', ',')), skip_empty=True)

    hailstone_paths = [tuple(np.array(list(map(int, v)))
                             for v in p) for p in raw_input]

    necessary_paths = hailstone_paths[:3]
    # c + v * t_1 = c_1 + v_1 * t_1
    # c + v * t_2 = c_2 + v_2 * t_2
    # c + v * t_3 = c_3 + v_3 * t_3
    # c, v are vectors
    # c, v, t_1, t_2, t_3 are unknown
    # For i=1,2,3:
    # c_i + v_i * t_i = c + v * t_i
    # ->
    # c_i - c = (v - v_i) * t_i
    # ->
    # t_i = (c_i - c) / (v - v_i)
    # eliminate with z coord
    # ->
    # (c_i_z - c_z) / (v_z - v_i_z) = (c_i_x - c_x) / (v_x - v_i_x)
    # (c_i_z - c_z) / (v_z - v_i_z) = (c_i_y - c_y) / (v_y - v_i_y)
    # ->
    # (c_i_z - c_z) * (v_y - v_i_y) = (c_i_y - c_y) * (v_z - v_i_z)
    # (c_i_z - c_z) * (v_x - v_i_x) = (c_i_x - c_x) * (v_z - v_i_z)
    # ->
    # c_i_z * v_y - c_i_z * v_i_y - c_z * v_y + c_z * v_i_y = c_i_y * v_z - c_i_y * v_i_z - c_y * v_z + c_y * v_i_z
    # c_i_z * v_x - c_i_z * v_i_x - c_z * v_x + c_z * v_i_x = c_i_x * v_z - c_i_x * v_i_z - c_x * v_z + c_x * v_i_z
    # ->
    # c_i_z * v_y - c_z * v_y + c_z * v_i_y  - c_i_y * v_z + c_y * v_z - c_y * v_i_z = c_i_z * v_i_y - c_i_y * v_i_z
    # c_i_z * v_x - c_z * v_x + c_z * v_i_x  - c_i_x * v_z + c_x * v_z - c_x * v_i_z = c_i_z * v_i_x - c_i_x * v_i_z
    # ->
    # (c_i_z - c_z) * v_y + v_i_y * c_z + (c_y - c_i_y) * v_z - v_i_z * c_y = c_i_z * v_i_y - c_i_y * v_i_z
    # (c_i_z - c_z) * v_x + v_i_x * c_z + (c_x - c_i_x) * v_z - v_i_z * c_x = c_i_z * v_i_x - c_i_x * v_i_z

    # c + v * t_1 = c_1 + v_1 * t_1
    # c + v * t_2 = c_2 + v_2 * t_2
    # c + v * t_3 = c_3 + v_3 * t_3
    # ->
    # c + (v - v_1) * t_1 = c_1
    # c + (v - v_2) * t_2 = c_2
    # c + (v - v_3) * t_3 = c_3
    # -> for eq i:
    # [I (v - v_i)] . [c t_i]^T = c_i
    # [1 0 0 (v_x - v_i_x)]
    # [0 1 0 (v_y - v_i_y)] . [c_x c_y c_z t_i]^T = c_i
    # [0 0 1 (v_z - v_i_z)]
    # ->
    # [1 0 0 v_x]   [1 0 0 -v_i_x]
    # [0 1 0 v_y] . [0 1 0 -v_i_y] . [c_x c_y c_z t_i]^T = c_i
    # [0 0 1 v_z]   [0 0 1 -v_i_z]
    #               [0 0 0 1]
    # ->
    # [v_x v_y v_z 1]
    return 0


class VecNet(nn.Module):
    def __init__(self, init_pos: torch.Tensor, init_dir: torch.Tensor):
        super().__init__()
        self.c = nn.Parameter(init_pos)
        self.v = nn.Parameter(init_dir)

    def forward(self, curr_vec_pos: torch.Tensor, curr_vec_dir: torch.Tensor) -> torch.Tensor:

        c_diff = self.c - curr_vec_pos
        v_diff = self.v - curr_vec_dir
        return torch.sqrt((c_diff - v_diff * (torch.dot(c_diff, v_diff) / torch.dot(v_diff, v_diff))).pow(2).sum())


def calc_throw_pos_ml(filename: str, min_coord: int, max_coord: int, num_dims: int) -> int:
    raw_input = parse_file_lines(
        Path(__file__).parent / filename, ('@', (',', ',')), skip_empty=True)

    hailstone_paths = [tuple(torch.Tensor(list(map(int, v)))
                             for v in p) for p in raw_input]

    # c + v * t_i = c_i + v_i * t_i
    # Distance between two points:
    # diff = sqrt((c - c_i + (v - v_i) * t_i)^2)
    # Find min d:
    # Same as finding min d^2:
    # d^2 = e = (c - c_i + (v - v_i) * t_i)^2
    # d e / d t_i = 2 * (c - c_i + (v - v_i) * t_i) * (v - v_i)
    # Set to 0, solve for t_i:
    # 0 = 2 * (c - c_i + (v - v_i) * t_i) * (v - v_i)
    # ->
    # 0 = (c - c_i + (v - v_i) * t_i) * (v - v_i)
    # ->
    # 0 = (c - c_i) * (v - v_i) + (v - v_i)^2 * t_i
    # ->
    # t_i = - (c - c_i) * (v - v_i) / (v - v_i)^2
    # Therefore min diff is:
    # sqrt((c - c_i - (c - c_i) * (v - v_i) / (v - v_i)^2)^2)

    vec_model = VecNet(torch.vstack([c for c, _ in hailstone_paths]).mean(
        0), torch.vstack([v for _, v in hailstone_paths]).mean(0))
    opt = torch.optim.Adam(vec_model.parameters(), lr=0.001)

    for i in range(1000000):
        opt.zero_grad()
        cum_loss = 0
        for c, v in hailstone_paths:
            loss = vec_model(c, v)
            loss.backward()
            cum_loss += loss.item()

        if torch.allclose(loss, torch.zeros(1)):
            print('Found solution: ', vec_model.c.data, vec_model.v.data)
            break

        opt.step()
        if i % 1000 == 0:
            print('Epoch loss: ', cum_loss / len(hailstone_paths))
            print('c: ', vec_model.c.data)
            print('v: ', vec_model.v.data)
        if cum_loss < 0.001:
            print('Try to round solution: ', vec_model.c.data, vec_model.v.data)
            vec_model.c.data = torch.round(vec_model.c.data)
            vec_model.v.data = torch.round(vec_model.v.data)

    return torch.sum(vec_model.c.abs())


if __name__ == "__main__":
    test_sol = calc_throw_pos_ml("data1_test.txt", 7, 27, 3)
    print(test_sol)
    assert test_sol == 47
    # Expected c: 24, 13, 10
    # Expected v: -3, 1, 2.
    real_sol = calc_throw_pos_ml(
        "data1_real.txt", 200000000000000, 400000000000000, 3)
    print(real_sol)
    # assert real_sol == 24192
