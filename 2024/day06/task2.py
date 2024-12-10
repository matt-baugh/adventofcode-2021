from enum import Enum
from time import time
from bisect import insort

from utils.file_utils import load_file


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def rotate(self):
        return Direction((self.value + 1) % 4)

    def along_row(self):
        return self == Direction.LEFT or self == Direction.RIGHT

    def increasing_coord(self):
        return self == Direction.RIGHT or self == Direction.DOWN

# (8, 2)


def construct_map(content: list[str]):
    rowwise_map = {}
    colwise_map = {}
    start_coord = None
    for i, l in enumerate(content):
        if i not in rowwise_map:
            rowwise_map[i] = []
        for j, c in enumerate(l):
            if j not in colwise_map:
                colwise_map[j] = []
            if c != '.':
                if c == '#':
                    rowwise_map[i].append(j)
                    colwise_map[j].append(i)

                else:
                    assert c == '^'
                    start_coord = (i, j)

    assert start_coord is not None

    return start_coord, rowwise_map, colwise_map


def count_antinodes(filename_str: str) -> int:
    content = load_file(filename_str)

    num_rows = len(content)
    num_cols = len(content[0])

    curr_coord, rowwise_map, colwise_map = construct_map(content)

    direction = Direction.UP
    visited_coords = set()
    attempted_coords = set()
    looping_coords = set()

    on_board = True
    while on_board:
        new_path, on_board = walk_ahead(num_rows, num_cols, curr_coord,
                                        rowwise_map, colwise_map, direction)

        # print("walkig from", curr_coord, "in direction", direction)
        # print("new path:", new_path)
        for step in new_path:

            step_coord, step_direction = step
            if step_coord != curr_coord and step_coord not in attempted_coords:

                # print('Step:', step_coor  d, step_direction)

                tmp_rowwise_map = rowwise_map.copy()
                if step_coord[0] not in tmp_rowwise_map:
                    tmp_rowwise_map[step_coord[0]] = [step_coord[1]]
                else:
                    tmp_rowwise_map[step_coord[0]
                                    ] = rowwise_map[step_coord[0]].copy()
                    insort(tmp_rowwise_map[step_coord[0]], step_coord[1])

                tmp_colwise_map = colwise_map.copy()
                if step_coord[1] not in tmp_colwise_map:
                    tmp_colwise_map[step_coord[1]] = [step_coord[0]]
                else:
                    tmp_colwise_map[step_coord[1]
                                    ] = colwise_map[step_coord[1]].copy()
                    insort(tmp_colwise_map[step_coord[1]], step_coord[0])

                if check_loop(num_rows, num_cols, curr_coord, tmp_rowwise_map, tmp_colwise_map, visited_coords, step_direction):
                    looping_coords.add(step_coord)

                attempted_coords.add(step_coord)

        curr_coord = new_path[-1][0]
        visited_coords |= set(new_path)
        direction = direction.rotate()

    return len(looping_coords)


def check_loop(
    num_rows: int,
    num_cols: int,
    curr_coord: tuple[int, int],
    rowwise_map: dict[int, list[int]],
    colwise_map: dict[int, list[int]],
    init_coords: set[tuple[tuple[int, int], Direction]],
    direction: Direction
) -> bool:
    logging = False  # 1 in rowwise_map[8]
    on_board = True
    visited_coords = set()
    while on_board:
        new_path, on_board = walk_ahead(num_rows, num_cols, curr_coord,
                                        rowwise_map, colwise_map, direction)
        if logging:
            print("Checking path:", new_path)
        new_path_s = set(new_path)

        if len(visited_coords & new_path_s) > 0 or len(init_coords & new_path_s) > 0:
            if logging:
                print("Looping path:", new_path, " with ", visited_coords)
            return True

        curr_coord = new_path[-1][0]
        visited_coords |= new_path_s
        direction = direction.rotate()

    return False


def walk_ahead(
    num_rows: int,
    num_cols: int,
    curr_coord: tuple[int, int],
    rowwise_map: dict[int, list[int]],
    colwise_map: dict[int, list[int]],
    direction: Direction
) -> tuple[list[tuple[tuple[int, int], Direction]], bool]:
    along_row = direction.along_row()
    curr_map = rowwise_map if along_row else colwise_map
    increasing_coord = direction.increasing_coord()

    curr_row, curr_col = curr_coord
    change_coord = curr_col if along_row else curr_row
    stable_coord = curr_row if along_row else curr_col

    new_coord = None
    if increasing_coord:
        # Get minimum value greater than current
        for coord in curr_map[stable_coord]:
            if coord > change_coord:
                new_coord = coord
                break
    else:
        # Get maximum value less than current
        for coord in curr_map[stable_coord]:
            if coord >= change_coord:
                break
            else:
                new_coord = coord

    if new_coord is None:
        on_board = False
        if along_row:
            new_coord = num_cols if increasing_coord else -1
        else:
            new_coord = num_rows if increasing_coord else -1
    else:
        on_board = True

    diff = -1 if increasing_coord else 1

    if along_row:
        curr_coord = (curr_row, new_coord + diff)
        new_path = [((curr_row, i), direction)
                    for i in range(curr_col, new_coord, -diff)]
    else:
        curr_coord = (new_coord + diff, curr_col)
        new_path = [((i, curr_col), direction)
                    for i in range(curr_row, new_coord, -diff)]

    return new_path, on_board


if __name__ == "__main__":

    print(count_antinodes("data1_test.txt"))
    start = time()
    print(count_antinodes("data1_real.txt"))
    print("Execution time:", time() - start)
