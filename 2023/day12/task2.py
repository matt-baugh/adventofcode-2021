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


def calc_combinations_opt(s_poss_groups: list[tuple[list[tuple[str, int]], bool]], s_target_groups: list[int]) -> int:

    if len(s_poss_groups) == 0:
        return int(len(s_target_groups) == 0)

    if len(s_target_groups) == 0:
        return int(not any([g[1] for g in s_poss_groups]))

    res = 0

    group1_subgroups, hash_in_group1 = s_poss_groups[0]
    assert len(group1_subgroups) > 0

    if not hash_in_group1:
        res += calc_combinations_opt(s_poss_groups[1:], s_target_groups)

    curr_target_group = s_target_groups[0]

    subgroup1_char, subgroup1_count = group1_subgroups[0]
    group1_other_subgroups = group1_subgroups[1:]

    if subgroup1_char == '#':
        if subgroup1_count > curr_target_group:
            return res

        hash_in_other_subgroups = any(
            sg[0] == '#' for sg in group1_other_subgroups)
        if subgroup1_count == curr_target_group:
            if len(group1_other_subgroups) == 0:
                return res + calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])
            else:
                subgroup2_char, subgroup2_count = group1_other_subgroups[0]
                assert subgroup2_char == '?'

                if subgroup2_count > 1:
                    # Subtract 1 to separate the subgroup we've found from the rest
                    edited_subgroup2 = (subgroup2_char, subgroup2_count - 1)
                    return res + calc_combinations_opt([([edited_subgroup2] + group1_other_subgroups[1:], hash_in_other_subgroups)] + s_poss_groups[1:],
                                                       s_target_groups[1:])
                elif subgroup2_count == 1:

                    # Skip the entire subgroup
                    if len(group1_other_subgroups) == 1:
                        return res + calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])
                    else:
                        return res + calc_combinations_opt([(group1_other_subgroups[1:], hash_in_other_subgroups)] + s_poss_groups[1:],
                                                           s_target_groups[1:])
                else:
                    assert False, 'Subgroup count cannot be less than 1'
        else:
            # subgroup1_count < curr_target_group

            curr_target_group_left = curr_target_group - subgroup1_count

            group1_extra_subgroups = group1_subgroups[1:]

            while curr_target_group_left > 0:
                if len(group1_extra_subgroups) == 0:
                    return res
                _, subgroup2_count = group1_extra_subgroups[0]
                if subgroup2_count > curr_target_group_left:
                    group1_extra_subgroups[0] = (
                        subgroup2_char, subgroup2_count - curr_target_group_left)
                    break
                curr_target_group_left -= subgroup2_count
                group1_extra_subgroups = group1_extra_subgroups[1:]

            if group1_extra_subgroups == []:
                return res + calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])

            subgroup2_char, subgroup2_count = group1_extra_subgroups[0]
            if subgroup2_char == '#':
                return res

            assert subgroup2_char == '?'
            if subgroup2_count > 1:
                group1_extra_subgroups[0] = (
                    subgroup2_char, subgroup2_count - 1)
                return res + calc_combinations_opt([(group1_extra_subgroups, any(c == '#' for c, _ in group1_extra_subgroups))] + s_poss_groups[1:],
                                                   s_target_groups[1:])

            else:
                assert subgroup2_count == 1
                if len(group1_extra_subgroups) == 1:
                    return res + calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])
                else:
                    return res + calc_combinations_opt([(group1_extra_subgroups[1:], any(c == '#' for c, _ in group1_extra_subgroups[1:]))] + s_poss_groups[1:],
                                                       s_target_groups[1:])

    else:
        assert subgroup1_char == '?'

        # Consider all cases which keep target group within current subgroup with a space afterwards
        if subgroup1_count > curr_target_group:
            for i in range(subgroup1_count - curr_target_group):
                # Subtract 1 to separate the subgroup we've found from the rest
                extra_subgroup_chars = subgroup1_count - curr_target_group - i - 1
                if extra_subgroup_chars > 0:
                    res += calc_combinations_opt([([(subgroup1_char, extra_subgroup_chars)] + group1_other_subgroups, hash_in_group1)] + s_poss_groups[1:],
                                                 s_target_groups[1:])
                else:
                    assert extra_subgroup_chars == 0, f'Subgroup count cannot be less than 0: {extra_subgroup_chars}'
                    if len(group1_other_subgroups) == 0:
                        # This group is exhausted, move to next
                        res += calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])
                    else:
                        # Other subgroups exist, consider them
                        res += calc_combinations_opt([(group1_other_subgroups, hash_in_group1)] + s_poss_groups[1:],
                                                     s_target_groups[1:])
        
        # Consider case where target group is tail of current subgroup             
        if subgroup1_count >= curr_target_group:
            if len(group1_other_subgroups) == 0:
                res += calc_combinations_opt(s_poss_groups[1:], s_target_groups[1:])
            else:
                res += calc_combinations_opt([(group1_other_subgroups, hash_in_group1)] + s_poss_groups[1:],
                                             s_target_groups[1:])
                        
        
        
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

                comb_sum += calc_combinations_opt(
                    poss_comb[arr_prefix_groups_starts[-1]:], s_groups[num_found_groups-1:])
            else:
                # arr_prefix[-1] == '.'
                if arr_prefix_groups[-1] != s_groups[num_found_groups-1]:
                    continue

                comb_sum += calc_combinations_opt(
                    poss_comb[next_opt_spr:], s_groups[num_found_groups:])

        else:
            comb_sum += calc_combinations_opt(
                poss_comb[next_opt_spr:], s_groups)

    return comb_sum


def get_contiguous_chars(s: str) -> list[tuple[str, int]]:
    res = []
    curr_char = None
    curr_count = 0
    for c in s:
        if c == curr_char:
            curr_count += 1
        else:
            if curr_char is not None:
                res.append([curr_char, curr_count])
            curr_char = c
            curr_count = 1
    res.append([curr_char, curr_count])
    return res


def sum_possible_arrangements(filename: str, num_repeats: int) -> int:
    springs_info = parse_file_lines(
        Path(__file__).parent / filename, (None, (None, ',')))

    assert num_repeats > 0
    total_arrangements = 0
    for s_arrangement, s_target_groups in tqdm(springs_info):
        s_arrangement = '?'.join(s_arrangement * num_repeats)
        s_possible_groups = [(get_contiguous_chars(g), '#' in g)
                             for g in s_arrangement.split('.') if g != '']
        s_target_groups = [int(s) for s in s_target_groups] * num_repeats

        line_res = calc_combinations_opt(s_possible_groups, s_target_groups)
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
    test_sol = sum_possible_arrangements("data1_test.txt", 5)
    print(test_sol)
    assert test_sol == 525152
    print(sum_possible_arrangements("data1_real.txt", 5))
