from enum import Enum
from time import time

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


def construct_map(content: list[str]):
    rowwise_map = {}
    colwise_map = {}
    start_coord = None
    for i, l in enumerate(content):
        for j, c in enumerate(l):
            if c != '.':
                if c == '#':
                    if i not in rowwise_map:
                        rowwise_map[i] = []
                    rowwise_map[i].append(j)

                    if j not in colwise_map:
                        colwise_map[j] = []
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

    visited_coords = {curr_coord}

    direction = Direction.UP

    on_board = True
    while on_board:
        along_row = direction.along_row()
        curr_map = rowwise_map if along_row else colwise_map
        increasing_coord = direction.increasing_coord()

        curr_row, curr_col = curr_coord
        change_coord = curr_col if along_row else curr_row
        stable_coord = curr_row if along_row else curr_col

        # print(curr_coord, ' changing ', change_coord, ' along row ', along_row,
        #       ' increasing coord ', increasing_coord)

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

        diff = -1 if increasing_coord else 1

        if along_row:
            curr_coord = (curr_row, new_coord + diff)
            visited_coords |= {(curr_row, i)
                               for i in range(curr_col, new_coord, -diff)}
        else:
            curr_coord = (new_coord + diff, curr_col)
            visited_coords |= {(i, curr_col)
                               for i in range(curr_row, new_coord, -diff)}

        direction = direction.rotate()
        # print(len(visited_coords), ':', visited_coords)

    return len(visited_coords)


if __name__ == "__main__":

    print(count_antinodes("data1_test.txt"))
    start = time()
    print(count_antinodes("data1_real.txt"))
    print("Execution time:", time() - start)
