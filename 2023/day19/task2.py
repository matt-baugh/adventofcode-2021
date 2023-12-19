from pathlib import Path
from operator import mul
from functools import reduce

from utils.file_utils import load_file, chunk_input, split_str

PRINT = False

ACCEPTED = 'A'
REJECTED = 'R'
PART_RESULTS = {ACCEPTED, REJECTED}

RATING_VAR_INDEX = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}


def calc_num_accepted_combinations(filename: str) -> int:

    raw_input = load_file(Path(__file__).parent / filename)

    raw_workflows, _ = chunk_input(raw_input, "")

    workflows = {}
    for r_wf in raw_workflows:
        wf_id, wf_content = r_wf.split("{")
        wf_content = wf_content[:-1]

        curr_workflow = []
        last_rule = len(wf_content.split(","))
        for i, wf_rule in enumerate(wf_content.split(",")):
            if ':' in wf_rule:
                assert i < last_rule - 1
                wf_cond, wf_rule_res = tuple(wf_rule.split(":"))
                wf_cond_var = wf_cond[0]
                wf_cond_op = wf_cond[1]
                wf_cond_val = int(wf_cond[2:])
                curr_workflow.append(
                    (wf_cond_var, wf_cond_op, wf_cond_val, wf_rule_res))
            else:
                assert i == last_rule - 1
                curr_workflow.append(wf_rule)

        workflows[wf_id] = curr_workflow

    def traverse_rules(rule_id: str, curr_ranges: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]) \
            -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]]:

        if rule_id == ACCEPTED:
            return [curr_ranges]
        elif rule_id == REJECTED:
            return []

        curr_workflow = workflows[rule_id]
        accepted_ranges = []

        for wf_rule in curr_workflow:
            if isinstance(wf_rule, tuple):
                wf_cond_var, wf_cond_op, wf_cond_val, wf_rule_res = wf_rule
                wf_cond_var_i = RATING_VAR_INDEX[wf_cond_var]
                wf_cond_var_range = curr_ranges[wf_cond_var_i]
                if wf_cond_op == '<':
                    split_val = min(wf_cond_var_range[1], wf_cond_val - 1)
                    curr_wf_cond_var_range = (wf_cond_var_range[0], split_val)
                    other_wf_cond_range = (split_val + 1, wf_cond_var_range[1])
                else:
                    assert wf_cond_op == '>'
                    split_val = max(wf_cond_var_range[0], wf_cond_val + 1)
                    curr_wf_cond_var_range = (split_val, wf_cond_var_range[1])
                    other_wf_cond_range = (wf_cond_var_range[0], split_val - 1)

                if curr_wf_cond_var_range[0] <= curr_wf_cond_var_range[1]:
                    accepted_ranges.append(traverse_rules(wf_rule_res, curr_ranges[:wf_cond_var_i] + (
                        curr_wf_cond_var_range,) + curr_ranges[wf_cond_var_i + 1:]))

                if other_wf_cond_range[0] <= other_wf_cond_range[1]:
                    curr_ranges = curr_ranges[:wf_cond_var_i] + \
                        (other_wf_cond_range,) + \
                        curr_ranges[wf_cond_var_i + 1:]
                else:
                    # No need to continue accumulating ranges
                    break
            else:
                accepted_ranges.append(traverse_rules(wf_rule, curr_ranges))

        return [r for r_list in accepted_ranges for r in r_list]

    overlapping_accepted_ranges = traverse_rules(
        'in', ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))

    ranges_sum = sum(reduce(mul, [ub - lb + 1 for lb, ub in range_bounds])
                     for range_bounds in overlapping_accepted_ranges)

    # Need to subtract double counted ranges
    for i, range1 in enumerate(overlapping_accepted_ranges):
        for range2 in overlapping_accepted_ranges[i + 1:]:
            overlap_range = tuple((max(lb1, lb2), min(ub1, ub2))
                                  for (lb1, ub1), (lb2, ub2) in zip(range1, range2))
            if all(lb <= ub for lb, ub in overlap_range):
                ranges_sum -= reduce(mul,
                                     [ub - lb + 1 for lb, ub in overlap_range])

    return ranges_sum


if __name__ == "__main__":
    test_sol = calc_num_accepted_combinations("data1_test.txt")
    print(test_sol)
    assert test_sol == 167409079868000
    real_sol = calc_num_accepted_combinations("data1_real.txt")
    print(real_sol)
    # assert real_sol == 492702
