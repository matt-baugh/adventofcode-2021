from time import time

from utils.file_utils import load_file


def walk_to_9(coord: tuple[int, int], top_map: list[list[int]], leads_to_map: dict[tuple[int, int], set[tuple[int, int]]]) -> set[tuple[int, int]]:

    if coord in leads_to_map:
        return leads_to_map[coord]

    i, j = coord

    height = top_map[i][j]

    if height == 9:
        reachable = {coord}
        leads_to_map[coord] = reachable
        return reachable

    reachable = set()
    for i_diff, j_diff in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_i = i + i_diff
        new_j = j + j_diff

        if new_i >= 0 and new_i < len(top_map) and new_j >= 0 and new_j < len(top_map[0]) and top_map[new_i][new_j] == (height + 1):
            reachable |= walk_to_9((new_i, new_j), top_map, leads_to_map)

    leads_to_map[coord] = reachable
    return reachable


def sum_scores(filename_str: str) -> int:
    content = load_file(filename_str)

    top_map = [[-1 if c == '.' else int(c) for c in l]for l in content]

    start_coords = []
    for i, row in enumerate(top_map):
        for j, h in enumerate(row):
            if h == 0:
                start_coords.append((i, j))

    leads_to_map = {}
    scores = 0
    for c in start_coords:
        scores += len(walk_to_9(c, top_map, leads_to_map))

    # print(leads_to_map)

    return scores


if __name__ == "__main__":

    print(sum_scores("data1_test.txt"))
    start = time()
    print(sum_scores("data1_real.txt"))
    print("Execution time:", time() - start)
