from bisect import insort
from pathlib import Path
from typing import Literal, Union


from utils.file_utils import load_file, chunk_input, split_str

PRINT = False

ACCEPTED = 'A'
REJECTED = 'R'
PART_RESULTS = {ACCEPTED, REJECTED}


def calc_rating_sum(filename: str) -> int:

    raw_input = load_file(Path(__file__).parent / filename)

    raw_workflows, raw_parts = chunk_input(raw_input, "")

    workflows = {}
    for r_wf in raw_workflows:
        wf_id, wf_content = r_wf.split("{")
        wf_content = wf_content[:-1]

        curr_workflow = []
        last_rule = len(wf_content.split(","))
        for i, wf_rule in enumerate(wf_content.split(",")):
            if ':' in wf_rule:
                assert i < last_rule - 1
                curr_workflow.append(tuple(wf_rule.split(":")))
            else:
                assert i == last_rule - 1
                curr_workflow.append(wf_rule)

        workflows[wf_id] = curr_workflow

    parts_sum = 0

    for r_p in raw_parts:
        r_p = r_p[1:-1]
        (x_char, x), (m_char, m), (a_char, a), (s_char, s) = split_str(r_p, (",", ("=", "=", "=", "=")))
        assert x_char == "x" and m_char == "m" and a_char == "a" and s_char == "s", f"Invalid part: {r_p}"
        x, m, a, s = int(x), int(m), int(a), int(s)
        
        curr_workflow = 'in'
        
        while curr_workflow not in PART_RESULTS:
            curr_workflow_rules = workflows[curr_workflow]
            for wf_rule in curr_workflow_rules:
                if isinstance(wf_rule, tuple):
                    rule_cond, rule_res = wf_rule
                    if eval(rule_cond):
                        curr_workflow = rule_res
                        break
                else:
                    # Must be last one
                    curr_workflow = wf_rule
                    break

        if curr_workflow == ACCEPTED:
            parts_sum += x + m + a + s

    return parts_sum


if __name__ == "__main__":
    test_sol = calc_rating_sum("data1_test.txt")
    print(test_sol)
    assert test_sol == 19114
    real_sol = calc_rating_sum("data1_real.txt")
    print(real_sol)
    assert real_sol == 492702
