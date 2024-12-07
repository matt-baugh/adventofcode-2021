import re

from utils.file_utils import load_file


def count_safe(filename_str: str) -> int:
    content = load_file(filename_str)

    total = 0

    for l in content:
        for exp in re.findall(r"mul\((\d+),(\d+)\)", l):
            total += int(exp[0]) * int(exp[1])

    return total


if __name__ == "__main__":
    print(count_safe("data1_test.txt"))
    print(count_safe("data1_real.txt"))
    # print(count_safe("data1_test.txt", True))
    # print(count_safe("data1_real.txt", True))
