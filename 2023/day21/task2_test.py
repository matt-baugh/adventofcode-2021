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
    last_step_map = None
    last_last_step_map = None

    for i in range(num_steps):
        last_last_step_map = last_step_map
        last_step_map = step_map.clone()
        step_map = F.conv2d(step_map, step_kernel, padding=1)
        step_map[rock_map == 1] = 0
        step_map[step_map > 0] = 1
        if last_last_step_map is not None and torch.equal(last_last_step_map, step_map):
            print("Found loop, required steps: ", i)
            print('last step map sum: ', last_step_map.sum())
            print('step map sum: ', step_map.sum())

    return int(step_map.sum())


if __name__ == "__main__":
    # test_sol = calc_num_locations("data1_test.txt", 100000000)
    # print(test_sol)
    # assert test_sol == 16
    real_sol = calc_num_locations("data1_real.txt", 135)
    # print(real_sol)
