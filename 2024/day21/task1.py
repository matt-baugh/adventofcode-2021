from typing import Union

from utils.file_utils import load_file

LEFT = '<'
RIGHT = '>'
UP = '^'
DOWN = 'v'
PRESS = 'A'

# Num Keypad
# 7 8 9
# 4 5 6
# 1 2 3
#   0 A
num_keypad: dict[str, tuple[tuple[int, int], set[str]]] = {
    '7': ((0, 0), {DOWN, RIGHT}),
    '8': ((0, 1), {DOWN, LEFT, RIGHT}),
    '9': ((0, 2), {DOWN, LEFT}),
    '4': ((1, 0), {UP, DOWN, RIGHT}),
    '5': ((1, 1), {UP, DOWN, LEFT, RIGHT}),
    '6': ((1, 2), {UP, DOWN, LEFT}),
    '1': ((2, 0), {UP, RIGHT}),
    '2': ((2, 1), {UP, DOWN, LEFT, RIGHT}),
    '3': ((2, 2), {UP, DOWN, LEFT}),
    '0': ((3, 1), {UP, RIGHT}),
    'A': ((3, 2), {UP, LEFT}),
}

# Directional Keypad
#   ^ A
# < v >
dir_keypad: dict[str, tuple[tuple[int, int], set[str]]] = {
    UP: ((0, 1), {DOWN, RIGHT}),
    PRESS: ((0, 2), {DOWN, LEFT}),
    LEFT: ((1, 0), {RIGHT}),
    DOWN: ((1, 1), {UP, LEFT, RIGHT}),
    RIGHT: ((1, 2), {UP, LEFT}),
}


def reverse_direction(direction: str) -> str:
    if direction == UP:
        return DOWN
    if direction == DOWN:
        return UP
    if direction == LEFT:
        return RIGHT
    if direction == RIGHT:
        return LEFT

    raise ValueError(f"Invalid direction: {direction}")


def get_paths(start: str, end: str, keypad: dict[str, tuple[tuple[int, int], set[str]]]) \
        -> list[str]:
    if start == end:
        return []
    assert start in keypad
    assert end in keypad

    (s_i, s_j), start_possible_moves = keypad[start]
    (e_i, e_j), _ = keypad[end]

    required_moves = []
    if e_i > s_i:
        required_moves.append((DOWN, e_i - s_i))
    elif e_i < s_i:
        required_moves.append((UP, s_i - e_i))

    if e_j > s_j:
        required_moves.append((RIGHT, e_j - s_j))
    elif e_j < s_j:
        required_moves.append((LEFT, s_j - e_j))

    assert len(required_moves) == 1 or len(required_moves) == 2, f"Invalid from {
        start} to {end}; required moves: {required_moves}"
    if len(required_moves) == 1:
        return [required_moves[0][0] * required_moves[0][1]]

    possible_paths = []
    # Try vertical first:
    if required_moves[0][0] in start_possible_moves and reverse_direction(required_moves[1][0]) in start_possible_moves:
        possible_paths.append(
            required_moves[0][0] * required_moves[0][1] + required_moves[1][0] * required_moves[1][1])

    # Try horizontal next:
    if required_moves[1][0] in start_possible_moves and reverse_direction(required_moves[0][0]) in start_possible_moves:
        possible_paths.append(
            required_moves[1][0] * required_moves[1][1] + required_moves[0][0] * required_moves[0][1])

    assert len(possible_paths) >= 1, \
        f"Failed to find path from {start} to {end}; moves: {required_moves}"

    return possible_paths


def compute_code_paths(code: list[str], keypad: dict[str, tuple[tuple[int, int], set[str]]]) -> list[str]:

    return [get_paths(k1, k2, keypad)
            for k1, k2 in zip('A' + code, code)]


def interp_press_keys(code: Union[list, str]):
    if isinstance(code, str):
        return PRESS.join(code) + PRESS

    return [interp_press_keys(c) for c in code]


def compute_all_dir_paths(code: Union[list, str]) -> list[str]:

    if isinstance(code, str):
        return compute_code_paths(code, dir_keypad)

    return [compute_code_paths(c, dir_keypad) for c in code]


def compute_complexities(filename_str: str) -> int:
    content = load_file(filename_str)

    complexity_sum = 0
    for num_code in content:
        curr_paths = [get_paths(k1, k2, num_keypad)
                      for k1, k2 in zip('A' + num_code, num_code)]

        for i in range(2):
            # Add 'press' buttons between each key code
            curr_paths = interp_press_keys(curr_paths)
            curr_paths = compute_all_dir_paths(curr_paths)

    return 0


if __name__ == "__main__":

    test_res = compute_complexities("data1_test.txt")
    assert test_res == 126384, f"Expected 126384, got {test_res}"
    # start = time()
    # print(compute_complexities("data1_real.txt"))
    # print("Execution time:", time() - start)
