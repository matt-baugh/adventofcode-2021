from pathlib import Path

from utils.file_utils import parse_file_lines


def sum_scratch_points(filename: str):    
    parsed_input = parse_file_lines(Path(__file__).parent / filename, split_val=(':', (None, ('|', (None, None)))))

    total = 0
    for _, (win_nums, my_nums) in parsed_input:
        num_matches = len(set(win_nums).intersection(set(my_nums)))
        if num_matches > 0:
            total += 2 ** (num_matches - 1)
    return total


if __name__ == "__main__":
    print(sum_scratch_points("data1_test.txt"))
    print(sum_scratch_points("data1_real.txt"))
