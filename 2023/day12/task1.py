from pathlib import Path

from tqdm import tqdm

from utils.file_utils import parse_file_lines

PRINT = False

def find_groups(s_arrangement: str) -> list[int]:
    s_groups = []
    s_groups_starts = []
    curr_group = 0
    curr_group_start = None
    for i, s in enumerate(s_arrangement):
        if s == '#':
            curr_group += 1
            if curr_group_start is None:
                curr_group_start = i
        elif curr_group > 0:
            s_groups.append(curr_group)
            s_groups_starts.append(curr_group_start)
            curr_group = 0
            curr_group_start = None
    if curr_group > 0:
        s_groups.append(curr_group)
        s_groups_starts.append(curr_group_start)
    return s_groups, s_groups_starts


def calc_combinations(s_arrangement: str, s_groups: list[int]) -> int:
    optional_spr_i = s_arrangement.find('?')
    assert optional_spr_i != -1

    comb_sum = 0
    for opt in ['.', '#']:
        poss_comb = s_arrangement[:optional_spr_i] + \
            opt + s_arrangement[optional_spr_i+1:]

        next_opt_spr = poss_comb.find('?')

        if next_opt_spr == -1:
            valid_comb = find_groups(poss_comb)[0] == s_groups
            if PRINT and valid_comb:
                print(poss_comb)
            comb_sum += int(valid_comb)
            continue

        arr_prefix = poss_comb[:next_opt_spr]
        arr_prefix_groups, arr_prefix_groups_starts = find_groups(arr_prefix)
        num_found_groups = len(arr_prefix_groups)

        if num_found_groups > len(s_groups):
            continue

        if num_found_groups != 0:

            if arr_prefix_groups[:-1] != s_groups[:max(num_found_groups-1, 0)]:
                continue

            if arr_prefix[-1] == '#':
                if arr_prefix_groups[-1] > s_groups[num_found_groups-1]:
                    continue

                comb_sum += calc_combinations(poss_comb[arr_prefix_groups_starts[-1]:], s_groups[num_found_groups-1:])
            else:
                # arr_prefix[-1] == '.'
                if arr_prefix_groups[-1] != s_groups[num_found_groups-1]:
                    continue

                comb_sum += calc_combinations(
                    poss_comb[next_opt_spr:], s_groups[num_found_groups:])

        else:
            comb_sum += calc_combinations(poss_comb[next_opt_spr:], s_groups)

    return comb_sum


def sum_possible_arrangements(filename: str, num_repeats: int) -> int:
    springs_info = parse_file_lines(
        Path(__file__).parent / filename, (None, (None, ',')))

    assert num_repeats > 0
    total_arrangements = 0
    for s_arrangement, s_groups in tqdm(springs_info):
        s_arrangement = '?'.join(s_arrangement * num_repeats)
        s_groups = [int(s) for s in s_groups] * num_repeats

        line_res = calc_combinations(s_arrangement, s_groups)
        if PRINT:
            print('line_res', line_res)

        total_arrangements += line_res
    return total_arrangements


if __name__ == "__main__":
    test_sol = sum_possible_arrangements("data1_test.txt", 1)
    print(test_sol)
    assert test_sol == 21
    real_sol = sum_possible_arrangements("data1_real.txt", 1)
    print(real_sol)
    assert real_sol == 6935
