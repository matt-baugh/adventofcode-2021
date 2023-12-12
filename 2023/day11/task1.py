from pathlib import Path

from utils.file_utils import load_file


def sum_shortest_paths(filename: str, empty_size: int) -> int:
    file_lines = load_file(Path(__file__).parent / filename)

    galaxy_coords = [(row, col) for row, line in enumerate(file_lines)
                     for col, c in enumerate(line) if c == '#']

    all_galaxy_rows = set(row for row, _ in galaxy_coords)
    all_galaxy_cols = set(col for _, col in galaxy_coords)
    empty_rows = set(range(len(file_lines))) - all_galaxy_rows
    empty_cols = set(range(len(file_lines[0]))) - all_galaxy_cols

    shortest_paths_sum = 0
    for i, (row1, col1) in enumerate(galaxy_coords):
        for row2, col2 in galaxy_coords[i+1:]:
            max_row = max(row1, row2)
            min_row = min(row1, row2)
            max_col = max(col1, col2)
            min_col = min(col1, col2)
            vert_dist = max_row - min_row + \
                len([r for r in empty_rows if min_row < r < max_row]) * (empty_size - 1)
            hor_dist = max_col - min_col + \
                len([c for c in empty_cols if min_col < c < max_col]) * (empty_size - 1)
            shortest_paths_sum += vert_dist + hor_dist

    return shortest_paths_sum


if __name__ == "__main__":
    test_sol = sum_shortest_paths("data1_test.txt", 2)
    print(test_sol)
    assert test_sol == 374
    print(sum_shortest_paths("data1_real.txt", 2))
