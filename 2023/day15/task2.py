from pathlib import Path

from task1 import hash_algorithm
from utils.file_utils import parse_file_lines

PRINT = False


def sum_hash_values(filename: str) -> int:
    hash_strs = parse_file_lines(Path(__file__).parent / filename, ',')[0]

    boxes = {i: {} for i in range(256)}
    for hash_str in hash_strs:
        instr_index = max(hash_str.find('-'), hash_str.find('='))
        label = hash_str[:instr_index]
        box_num = hash_algorithm(label)
        instr = hash_str[instr_index]
        if instr == '-' and label in boxes[box_num]:
            del boxes[box_num][label]
        elif instr == '=':
            focal_len = int(hash_str[instr_index + 1])
            assert focal_len != 0
            boxes[box_num][label] = focal_len
        # print([(l, b) for l, b in boxes.items() if b])

    return sum((i + 1) * (j + 1) * f for i in range(256) for j, f in enumerate(boxes[i].values()))


if __name__ == "__main__":
    test_sol = sum_hash_values("data1_test.txt")
    print(test_sol)
    assert test_sol == 145
    real_sol = sum_hash_values("data1_real.txt")
    print(real_sol)
    assert real_sol == 265345
