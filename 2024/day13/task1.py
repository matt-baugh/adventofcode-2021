import re
from time import time

from utils.file_utils import load_file, chunk_input


def parse_rules(rule_inputs: list[str]) -> dict[int, list[int]]:

    rules = []
    for r in rule_inputs:
        assert len(r) == 3
        rules.append([
            tuple(int(num) for num in re.findall(r'\d+', l))for l in r])

    return rules


def sum_claw_costs(filename_str: str, prize_offset: int = 0) -> int:

    content = load_file(filename_str)

    rule_inputs = chunk_input(content, "")

    rules = parse_rules(rule_inputs)

    result = 0

    for r in rules:
        a_x, a_y = r[0]
        b_x, b_y = r[1]
        p_x, p_y = r[2]

        p_x += prize_offset
        p_y += prize_offset

        determinant = a_x * b_y - b_x * a_y
        if determinant == 0:
            continue

        a_presses = (b_y * p_x - b_x * p_y) / determinant
        b_presses = (a_x * p_y - a_y * p_x) / determinant

        if a_presses < 0 or b_presses < 0:
            continue

        if prize_offset == 0 and (a_presses > 100 or b_presses > 100):
            continue

        if a_presses.is_integer() and b_presses.is_integer():
            result += 3 * a_presses + b_presses

    return result


if __name__ == "__main__":

    assert sum_claw_costs("data1_test.txt") == 480
    start = time()
    print(sum_claw_costs("data1_real.txt"))
    print("Execution time:", time() - start)

    print('Task 2 test: ', sum_claw_costs(
        "data1_test.txt", prize_offset=10000000000000))
    start = time()
    print(sum_claw_costs("data1_real.txt", prize_offset=10000000000000))
    print("Execution time:", time() - start)
