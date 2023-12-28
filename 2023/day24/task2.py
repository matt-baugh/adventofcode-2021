from pathlib import Path

from sympy import Eq, solve, symbols
from sympy.geometry import Point3D, Ray3D
# import torch
# import torch.nn as nn

from utils.file_utils import parse_file_lines

PRINT = False


def calc_throw_pos(filename: str, min_coord: int, max_coord: int, num_dims: int) -> int:
    raw_input = parse_file_lines(
        Path(__file__).parent / filename, ('@', (',', ',')), skip_empty=True)

    hailstone_paths = [tuple(tuple(map(int, v))
                             for v in p) for p in raw_input]

    necessary_paths = hailstone_paths[:3]
    # print(necessary_paths)
    hail_rays = [Ray3D(Point3D(origin), direction_ratio=Point3D(direction))
                   for origin, direction in necessary_paths]

# Define symbolic variables for the unknown origin and direction of the fourth ray
    x, y, z, dx, dy, dz = symbols('x y z dx dy dz')

    # Create the fourth ray with unknown origin and direction
    stone_ray = Ray3D(Point3D(x, y, z), direction_ratio=Point3D(dx, dy, dz))
    
    hail_ray_times = [symbols(f't_{i}') for i in range(3)]
    
    eqs = []
    for hr, hr_t in zip(hail_rays, hail_ray_times):
        eqs.extend([
            Eq(hr.source.x + hr_t * hr.direction.x, stone_ray.source.x + hr_t * stone_ray.direction.x),
            Eq(hr.source.y + hr_t * hr.direction.y, stone_ray.source.y + hr_t * stone_ray.direction.y),
            Eq(hr.source.z + hr_t * hr.direction.z, stone_ray.source.z + hr_t * stone_ray.direction.z)
        ])

# Solve the system of equations
    solution = solve(eqs, (x, y, z, dx, dy, dz, *hail_ray_times))
    print(solution)

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
    return sum(solution[0][:3])


# def batch_dot(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
#     return torch.sum(a * b, dim=1)


# class VecNet(nn.Module):
#     def __init__(self, init_pos: torch.Tensor, init_dir: torch.Tensor):
#         super().__init__()
#         self.c = nn.Parameter(init_pos)
#         self.v = nn.Parameter(init_dir)

#     def forward(self, curr_vec_pos: torch.Tensor, curr_vec_dir: torch.Tensor) -> torch.Tensor:

#         c_diff = self.c - curr_vec_pos
#         v_diff = self.v - curr_vec_dir
#         c_dot_v = batch_dot(c_diff, v_diff)
#         v_dot_v = batch_dot(v_diff, v_diff)
#         return torch.sqrt((c_diff - v_diff * (c_dot_v / v_dot_v)[..., None]).pow(2).sum(dim=1))


# def calc_throw_pos_ml(filename: str, min_coord: int, max_coord: int, num_dims: int, scale_factor: int) -> int:
#     raw_input = parse_file_lines(
#         Path(__file__).parent / filename, ('@', (',', ',')), skip_empty=True)

#     hailstone_paths = [tuple(torch.Tensor(list(map(int, v)))
#                              for v in p) for p in raw_input]
#     all_c = torch.vstack([c for c, _ in hailstone_paths]) / scale_factor
#     all_v = torch.vstack([v for _, v in hailstone_paths])

#     # c + v * t_i = c_i + v_i * t_i
#     # Distance between two points:
#     # diff = sqrt((c - c_i + (v - v_i) * t_i)^2)
#     # Find min d:
#     # Same as finding min d^2:
#     # d^2 = e = (c - c_i + (v - v_i) * t_i)^2
#     # d e / d t_i = 2 * (c - c_i + (v - v_i) * t_i) * (v - v_i)
#     # Set to 0, solve for t_i:
#     # 0 = 2 * (c - c_i + (v - v_i) * t_i) * (v - v_i)
#     # ->
#     # 0 = (c - c_i + (v - v_i) * t_i) * (v - v_i)
#     # ->
#     # 0 = (c - c_i) * (v - v_i) + (v - v_i)^2 * t_i
#     # ->
#     # t_i = - (c - c_i) * (v - v_i) / (v - v_i)^2
#     # Therefore min diff is:
#     # sqrt((c - c_i - (c - c_i) * (v - v_i) / (v - v_i)^2)^2)

#     vec_model = VecNet(all_c[0]*0.9 + all_c[1]*0.1, all_v.mean(0))
#     opt = torch.optim.Adam(vec_model.parameters(), lr=0.003)

#     best_loss = None
#     best_loss_epoch = None
#     start = time()
#     for i in range(1000000):
#         opt.zero_grad()
#         cum_loss = 0
#         # for c, v in hailstone_paths:
#         #     loss = vec_model(c, v)
#         #     loss.backward()
#         #     cum_loss += loss.item()
#         for _ in range(len(hailstone_paths) // 3):
#             rand_indices = torch.randperm(len(hailstone_paths))[:3]
#             loss = vec_model(all_c[rand_indices], all_v[rand_indices]).sum()
#             loss.backward()
#             cum_loss += loss.item()
#             opt.step()

#         if torch.allclose(loss, torch.zeros(1)):
#             print('Found solution: ', vec_model.c.data, vec_model.v.data)
#             break

#         if best_loss == None or cum_loss < best_loss - 0.001:
#             best_loss = cum_loss
#             best_loss_epoch = i
#         elif i - best_loss_epoch > 50000 and scale_factor > 1:
#             print('Loss did not improve for 10000 epochs, reversing scale factor')
#             scale_factor = scale_factor // 10
#             all_c *= 10
#             vec_model.c.data *= 10
#             best_loss_epoch = i  # Reset best loss epoch
#             best_loss = None

#         if i % 1000 == 0:
#             print()
#             print('Epoch: ', i, 'Time: ', time() - start)
#             print('Epoch loss: ', cum_loss / len(hailstone_paths))
#             print('c: ', vec_model.c.data)
#             print('v: ', vec_model.v.data)
#         if cum_loss < 0.001:
#             print('Try to round solution: ', vec_model.c.data, vec_model.v.data)
#             vec_model.c.data = torch.round(vec_model.c.data)
#             vec_model.v.data = torch.round(vec_model.v.data)

#     return torch.sum(vec_model.c.abs())


if __name__ == "__main__":
    test_sol = calc_throw_pos("data1_test.txt", 7, 27, 3)
    # test_sol = calc_throw_pos_ml("data1_test.txt", 7, 27, 3, scale_factor=1)
    print(test_sol)
    assert test_sol == 47
    # Expected c: 24, 13, 10
    # Expected v: -3, 1, 2.
    # real_sol = calc_throw_pos_ml(
    #     "data1_real.txt", 200000000000000, 400000000000000, 3, scale_factor=100000000000000)
    # local minima
    # c:  tensor([2.2035e+09, 3.1863e+09, 2.1019e+09])
    # v:  tensor([ 82.9921, -48.9944,  95.9804])
    real_sol = calc_throw_pos("data1_real.txt", 200000000000000, 400000000000000, 3)
    print(real_sol)
    assert real_sol == 664822352550558
