from pathlib import Path
from typing import Optional

from utils.file_utils import load_file

PRINT = False


def follow_path(maze: list[str], start_pos: tuple[int, int]) -> tuple[int, tuple[int, int]]:
    last_pos = None
    curr_pos = start_pos
    path_len = 1
    while True:
        c_i, c_j = curr_pos
        adj_pos = [(c_i + d_i, c_j + d_j)
                   for d_i, d_j in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        valid_pos = [p for p in adj_pos if 0 <= p[0] < len(maze) and 0 <= p[1] < len(maze[0])
                     and maze[p[0]][p[1]] == '.' and p != last_pos]
        if len(valid_pos) == 0:
            break
        elif len(valid_pos) == 1:
            last_pos = curr_pos
            curr_pos = valid_pos[0]
            path_len += 1
        else:
            raise ValueError("Invalid map, error at coord: " + str(curr_pos))

    return path_len, curr_pos


def find_next_paths(maze: list[str], start_pos: tuple[int, int]) -> list[tuple[int, int]]:
    assert maze[start_pos[0]][start_pos[1]] == '.'
    c_i, c_j = start_pos
    path_pos = [(c_i + 2 * d_i, c_j + 2 * d_j)
                for a, (d_i, d_j) in [('>', (0, 1)), ('v', (1, 0)), ('<', (0, -1)), ('^', (-1, 0))]
                if 0 <= (c_i + d_i) < len(maze) and 0 <= (c_j + d_j) < len(maze[0]) and maze[c_i + d_i][c_j + d_j] == a]
    for p_i, p_j in path_pos:
        assert maze[p_i][p_j] == '.'
    return path_pos


def input_to_graph(filename: str) -> dict[int, dict[int, int]]:
    maze = load_file(Path(__file__).parent / filename)
    graph: dict[str, dict[str, int]] = {}

    start_pos = (0, 1)

    pos_to_node = {start_pos: 0}

    start_path_len, star_path_end = follow_path(maze, start_pos)
    next_node_pos = find_next_paths(maze, star_path_end)
    assert len(
        next_node_pos) == 1, 'First node has more than one path: ' + str(next_node_pos)

    graph[0] = {1: start_path_len}
    pos_to_node[next_node_pos[0]] = 1
    graph[1] = {0: start_path_len}
    paths_to_process = [(1, c)
                        for c in find_next_paths(maze, next_node_pos[0])]
    last_node_id = 1
    while len(paths_to_process) > 0:
        node_from, path_start = paths_to_process[0]
        paths_to_process = paths_to_process[1:]

        path_len, path_end = follow_path(maze, path_start)
        path_len += 2  # Add one for first slope and previous node

        next_node_pos = find_next_paths(maze, path_end)
        if len(next_node_pos) == 0:
            # Reached end
            # Must be bottom of maze
            assert path_end == (
                len(maze) - 1, len(maze[0]) - 2), 'Unexpected end: ' + str(path_end)
            # Give end node id of -1
            graph[node_from][-1] = path_len
            continue

        for p in next_node_pos:
            if p not in pos_to_node:
                last_node_id += 1
                pos_to_node[p] = last_node_id
                paths_to_process.extend([(last_node_id, new_p)
                                        for new_p in find_next_paths(maze, p)])
                graph[last_node_id] = {}
            else:
                if PRINT:
                    print('Found existing node: ' + str(p))

            # Add another for outgoing slope
            graph[node_from][pos_to_node[p]] = path_len + 1
            graph[pos_to_node[p]][node_from] = path_len + 1

    return graph


def calc_longest_path(filename: str) -> Optional[int]:
    maze_graph = input_to_graph(filename)

    def find_longest_path(start_node: int, visited: set[int]) -> int:
        if start_node in visited:
            assert False, 'Loop detected'
        if start_node == -1:
            return 0
        visited.add(start_node)
        max_dist = None
        for n in maze_graph[start_node]:
            if n not in visited:
                max_from_n = find_longest_path(n, visited.copy())
                if max_from_n is not None and (max_dist is None or (maze_graph[start_node][n] + max_from_n) > max_dist):
                    max_dist = maze_graph[start_node][n] + max_from_n
        return max_dist

    return find_longest_path(0, set())


if __name__ == "__main__":
    test_sol = calc_longest_path("data1_test.txt")
    print(test_sol)
    assert test_sol == 154
    real_sol = calc_longest_path("data1_real.txt")
    print(real_sol)
    # assert real_sol == 524
