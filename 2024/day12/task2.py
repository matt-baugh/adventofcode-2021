from time import time

from utils.file_utils import load_file


def discover_region(start_coord: tuple[int, int], content: list[str]):

    num_rows = len(content)
    num_cols = len(content[0])

    region_plant = content[start_coord[0]][start_coord[1]]
    region_coords = {start_coord}
    region_frontier = {start_coord}
    perimeter_coords = set()

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
                    perimeter_coords.add(coord)

        region_frontier = new_frontier

    return region_plant, region_coords, perimeter_coords


offsets = [
    (-1, 0),  # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1)  # Left
]


def count_corners(perimeter_coords: set[tuple[int, int]], all_coords: set[tuple[int, int]]) -> int:
    # ...
    # .P.
    # ...
    corners = 0

    for i, j in perimeter_coords:

        up_in, right_in, down_in, left_in = [
            (i + offset[0], j + offset[1]) in all_coords for offset in offsets]
        print([up_in, right_in, down_in, left_in])

        # Check for outer corners
        for b1, b2 in [(up_in, right_in), (right_in, down_in), (down_in, left_in), (left_in, up_in)]:
            if not b1 and not b2:
                corners += 1

        # Check for inner corners
        if up_in and not right_in and (i - 1, j + 1) in all_coords:
            corners += 1
        if right_in and not down_in and (i + 1, j + 1) in all_coords:
            corners += 1
        if down_in and not left_in and (i + 1, j - 1) in all_coords:
            corners += 1
        if left_in and not up_in and (i - 1, j - 1) in all_coords:
            corners += 1

    print(f"Corners: {corners}")

    return corners


def sum_fences(filename_str: str) -> int:
    content = load_file(filename_str)

    num_rows = len(content)
    num_cols = len(content[0])
    remaining_nodes = {i: {j for j in range(
        num_cols)} for i in range(num_rows)}

    start_coord = (0, 0)

    total_fence_cost = 0
    while start_coord is not None:
        _, r_coords, r_perimeter = discover_region(start_coord, content)

        fence_cost = len(r_coords) * count_corners(r_perimeter, r_coords)
        print(f"Region: {r_coords}")
        print(f"Perimeter: {r_perimeter}")
        print(f"Fence cost: {fence_cost}")
        print()

        total_fence_cost += fence_cost
        for c_i, c_j in r_coords:
            remaining_nodes[c_i].remove(c_j)

        start_coord = None
        for i in range(num_rows):
            if len(remaining_nodes[i]) > 0:
                start_coord = (i, min(remaining_nodes[i]))
                break
    return total_fence_cost


if __name__ == "__main__":

    test_small_res = sum_fences("data1_test_small.txt")
    assert test_small_res == 80, f"Expected 80, but got {test_small_res}"

    test_within_res = sum_fences("data1_test_within.txt")
    assert test_within_res == 436, f"Expected 436, but got {test_within_res}"

    test_res = sum_fences("data1_test.txt")
    assert test_res == 1206, f"Expected 1206, but got {test_res}"
    start = time()
    print(sum_fences("data1_real.txt"))
    print("Execution time:", time() - start)
