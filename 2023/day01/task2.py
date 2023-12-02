import re

from day01.task1 import sum_first_and_last

str_to_number = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def find_all_numbers(line: str):

    nums = []
    num_str = [f'|(?=({k}))' for k in str_to_number.keys()]
    for i in re.findall(r"(\d)" + ''.join(num_str), line):

        real_res = [j for j in list(i) if j != ''][0]

        if real_res.isdigit():
            nums.append(int(real_res))
        else:
            nums.append(str_to_number[real_res])
    return nums

if __name__ == "__main__":
    print(sum_first_and_last("data2_test.txt", find_all_numbers))
    print(sum_first_and_last("data2_real.txt", find_all_numbers))
