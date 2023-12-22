from pathlib import Path

import torch
import torch.nn.functional as F

from utils.file_utils import load_file

PRINT = False


def calc_num_locations(filename: str, num_steps: int) -> int:

    raw_input = load_file(Path(__file__).parent / filename)

    rock_map = torch.Tensor(
        [[1 if c == '#' else 0 for c in line] for line in raw_input])

    start_pos = [(i, j) for i, r in enumerate(raw_input)
                 for j, c in enumerate(r) if c == 'S']
    assert len(start_pos) == 1
    start_pos = start_pos[0]

    step_map = torch.zeros_like(rock_map)
    step_map[start_pos] = 1

    step_kernel = torch.Tensor([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    
    rock_map = rock_map.unsqueeze(0).unsqueeze(0)
    step_map = step_map.unsqueeze(0).unsqueeze(0)
    step_kernel = step_kernel.unsqueeze(0).unsqueeze(0)

    for _ in range(num_steps):
        step_map = F.conv2d(step_map, step_kernel, padding=1)
        step_map[rock_map == 1] = 0
        step_map[step_map > 0] = 1

    return int(step_map.sum())


if __name__ == "__main__":
    test_sol = calc_num_locations("data1_test.txt", 6)
    print(test_sol)
    assert test_sol == 16
    real_sol = calc_num_locations("data1_real.txt", 64)
    print(real_sol)
