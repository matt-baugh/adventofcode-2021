from bisect import insort
from pathlib import Path
from typing import Literal, Union


from utils.file_utils import load_file

PRINT = False

VERT = 0
HOR = 1

DIR = Union[Literal[0], Literal[1]]


def get_next_pos(curr_pos_dir: tuple[tuple[int, int], DIR], input_shape: tuple[int, int], straight_move_range: int) \
        -> list[tuple[tuple[int, int], DIR]]:
    coord, in_dir = curr_pos_dir
    res = []
    out_dir = 1 - in_dir
    for i in range(1, straight_move_range + 1):
        if out_dir == VERT:
            if coord[0] + i < input_shape[0]:
                res.append(((coord[0] + i, coord[1]), out_dir))
            if coord[0] - i >= 0:
                res.append(((coord[0] - i, coord[1]), out_dir))
        elif in_dir == HOR:
            if coord[1] + i < input_shape[1]:
                res.append(((coord[0], coord[1] + i), out_dir))
            if coord[1] - i >= 0:
                res.append(((coord[0], coord[1] - i), out_dir))
        else:
            raise ValueError(f"Invalid direction: {in_dir}")

    return res


def calc_heat_loss(filename: str, straight_move_min: int, straight_move_max: int) -> int:
    raw_input = load_file(Path(__file__).parent / filename)

    cost_map = [list(map(int, r)) for r in raw_input]
    map_shape = (len(raw_input), len(raw_input[0]))

    visited_pos_dirs: set[tuple[tuple[int, int], DIR]] = {
        ((0, 0), HOR), ((0, 0), VERT)}

    frontier_costs: list[tuple[tuple[int, int], DIR], int] = []
    frontier_pos_dirs: set[tuple[tuple[int, int], DIR]] = set()

    def update_frontier(pos_dir: tuple[tuple[int, int], DIR], cost: int):
        if pos_dir not in visited_pos_dirs and pos_dir not in frontier_pos_dirs:

            insort(frontier_costs, (pos_dir, cost), key=lambda x: x[1])
            frontier_pos_dirs.add(pos_dir)
        elif pos_dir in frontier_pos_dirs:

            [curr_cost] = [c for p, c in frontier_costs if p == pos_dir]
            if curr_cost > cost:
                frontier_costs.remove((pos_dir, curr_cost))
                insort(frontier_costs, (pos_dir, cost), key=lambda x: x[1])

    h_cost = 0
    v_cost = 0
    # At the beginning we're in the top left, so we can only go right or down
    for i in range(1, straight_move_max + 1):
        h_cost += cost_map[0][i]
        v_cost += cost_map[i][0]

        if i >= straight_move_min:
            update_frontier(((0, i), HOR), h_cost)
            update_frontier(((i, 0), VERT), v_cost)

    if PRINT:
        print(f"Initial frontier: {frontier_costs}")
        print(f"Initial frontier pos dirs: {frontier_pos_dirs}")
        print(f"Initial visited: {visited_pos_dirs}")

    while len(frontier_costs) > 0:
        closest_pos_dir, lowest_cost = frontier_costs[0]

        if closest_pos_dir[0] == (map_shape[0] - 1, map_shape[1] - 1):
            return lowest_cost

        frontier_costs = frontier_costs[1:]
        frontier_pos_dirs.remove(closest_pos_dir)
        visited_pos_dirs.add(closest_pos_dir)

        curr_coord, in_dir = closest_pos_dir
        out_dir = 1 - in_dir
        pos_cost = lowest_cost
        neg_cost = lowest_cost
        for i in range(1, straight_move_max + 1):
            if out_dir == VERT:
                if curr_coord[0] + i < map_shape[0]:

                    pos_cost += cost_map[curr_coord[0] + i][curr_coord[1]]
                    if i >= straight_move_min:
                        update_frontier(
                            ((curr_coord[0] + i, curr_coord[1]), out_dir), pos_cost)
                if curr_coord[0] - i >= 0:

                    neg_cost += cost_map[curr_coord[0] - i][curr_coord[1]]
                    if i >= straight_move_min:
                        update_frontier(
                            ((curr_coord[0] - i, curr_coord[1]), out_dir), neg_cost)
            elif out_dir == HOR:
                if curr_coord[1] + i < map_shape[1]:

                    pos_cost += cost_map[curr_coord[0]][curr_coord[1] + i]
                    if i >= straight_move_min:
                        update_frontier(
                            ((curr_coord[0], curr_coord[1] + i), out_dir), pos_cost)
                if curr_coord[1] - i >= 0:

                    neg_cost += cost_map[curr_coord[0]][curr_coord[1] - i]
                    if i >= straight_move_min:
                        update_frontier(
                            ((curr_coord[0], curr_coord[1] - i), out_dir), neg_cost)
            else:
                raise ValueError(f"Invalid direction: {in_dir}")

    raise ValueError("No path found")


if __name__ == "__main__":
    test_sol = calc_heat_loss("data1_test.txt", 1, 3)
    print(test_sol)
    assert test_sol == 102
    real_sol = calc_heat_loss("data1_real.txt", 1, 3)
    print(real_sol)
    assert real_sol == 1244
