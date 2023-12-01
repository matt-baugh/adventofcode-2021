from pathlib import Path
import re

from utils.file_utils import load_file


def find_numbers(line: str):
    return [int(number) for number in re.findall(r"\d", line)]


def sum_first_and_last(filename: str, number_finder: callable):
    total = 0

    for line in load_file(Path(__file__).parent / filename):
        numbers = number_finder(line)
        total += numbers[0] * 10 + numbers[-1]

    return total

if __name__ == "__main__":
    print(sum_first_and_last("data1_test.txt", find_numbers))
    print(sum_first_and_last("data1_real.txt", find_numbers))
