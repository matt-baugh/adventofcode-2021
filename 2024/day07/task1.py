from time import time

from utils.file_utils import parse_file_lines


def calc_calibration(target: int, vals: list[int], enable_concat: bool) -> bool:

    possible_vals = {0}
    operations = [
        lambda a, b: a + b,
        lambda a, b: a * b
    ]
    if enable_concat:
        operations.append(lambda a, b: int(str(a) + str(b)))

    for new_val in vals:
        new_vals = set()

        for acc_val in possible_vals:

            for op in operations:
                op_res = op(acc_val, new_val)
                if op_res <= target:
                    new_vals.add(op_res)

        if len(new_vals) == 0:
            return False

        possible_vals = new_vals

    return target in possible_vals


def sum_calibration(filename_str: str, enable_concat: bool = False) -> int:
    content = parse_file_lines(filename_str, (":", (None, " ")))

    total = 0
    for line in content:
        target = int(line[0][0])
        vals = [int(i) for i in line[1][1:]]
        # print(target, vals)
        res = calc_calibration(target, vals, enable_concat)
        if res:
            total += target
        # print(line, '-', res)
        # print()

    return total


if __name__ == "__main__":

    print(sum_calibration("data1_test.txt"))
    start = time()
    print(sum_calibration("data1_real.txt"))
    print("Execution time:", time() - start)

    # task 2
    print(sum_calibration("data1_test.txt", enable_concat=True))
    start = time()
    print(sum_calibration("data1_real.txt", enable_concat=True))
    print("Execution time:", time() - start)
