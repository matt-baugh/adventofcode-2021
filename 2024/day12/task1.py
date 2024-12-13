from time import time

from utils.file_utils import load_file


def discover_region(start_coord: tuple[int, int], content: list[str]):

    num_rows = len(content)
    num_cols = len(content[0])

    region_plant = content[start_coord[0]][start_coord[1]]
    region_coords = {start_coord}
    region_frontier = {start_coord}
    perimeter = 0

    while len(region_frontier) != 0:
        new_frontier = set()
        for coord in region_frontier:
            for i, j in [(coord[0] - 1, coord[1]),
                         (coord[0] + 1, coord[1]),
                         (coord[0], coord[1] - 1),
                         (coord[0], coord[1] + 1)]:
                neighbour_coord = (i, j)
                if neighbour_coord in region_coords:
                    continue

                if 0 <= i < num_rows and 0 <= j < num_cols and content[i][j] == region_plant:
                    new_frontier.add(neighbour_coord)
                    region_coords.add(neighbour_coord)
                else:
                    perimeter += 1

        region_frontier = new_frontier

    return region_plant, region_coords, perimeter


def sum_fences(filename_str: str) -> int:
    content = load_file(filename_str)

    num_rows = len(content)
    num_cols = len(content[0])
    remaining_nodes = {i: {j for j in range(
        num_cols)} for i in range(num_rows)}

    start_coord = (0, 0)

    regions = {}
    total_fence_cost = 0
    while start_coord is not None:
        r_plant, r_coords, r_perimeter = discover_region(start_coord, content)

        total_fence_cost += len(r_coords) * r_perimeter
        for c_i, c_j in r_coords:
            remaining_nodes[c_i].remove(c_j)

        start_coord = None
        for i in range(num_rows):
            if len(remaining_nodes[i]) > 0:
                start_coord = (i, min(remaining_nodes[i]))
                break
    return total_fence_cost


if __name__ == "__main__":

    assert sum_fences("data1_test_small.txt") == 140
    assert sum_fences("data1_test_within.txt") == 772
    assert sum_fences("data1_test.txt") == 1930
    start = time()
    print(sum_fences("data1_real.txt"))
    print("Execution time:", time() - start)
