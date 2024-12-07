import re

from utils.file_utils import load_file


def sum_mul(filename_str: str) -> int:
    content = load_file(filename_str)

    total = 0

    enabled = True
    for l in content:
        for exp in re.findall(r"(mul\((\d+),(\d+)\))|(do(n\'t)?\(\))", l):
            if exp[0] != "" :
                if enabled:
                    total += int(exp[1]) * int(exp[2])
            elif exp[3] == "don't()":
                enabled = False
            elif exp[3] == "do()":
                enabled = True
            else:
                raise ValueError(f"Invalid expression: {exp}")
            # print(exp)
            # total += int(exp[0]) * int(exp[1])

    return total


if __name__ == "__main__":
    print(sum_mul("data2_test.txt"))
    print(sum_mul("data1_real.txt"))
    print(sum_mul("data2_real.txt"))
    # print(count_safe("data1_test.txt", True))
    # print(count_safe("data1_real.txt", True))
