import math
from pathlib import Path

from time import time

from utils.file_utils import load_file


def steps_to_reach(filename: str):
    file_lines = load_file(Path(__file__).parent / filename)

    path_instructions = file_lines[0]

    path_map = {}

    for l in file_lines[2:]:
        ws = l.split()
        # print(ws)
        path_map[ws[0]] = (ws[2][1:-1], ws[3][:-1])

    locs = [l for l in path_map.keys() if l[-1] == "A"]
    step = 0

    looping_locs_cache = {}
    print('Num possible locs:', len(path_map.keys()))

    path_len = len(path_instructions)

    start = time()

    num_loops = 0
    while True:

        curr_ends = []

        all_cached = True

        for loc in locs:
            if loc not in looping_locs_cache:
                all_cached = False
                interim_loc = loc
                poss_end_steps = []
                visited_locs = []
                for step in range(path_len):

                    if interim_loc[-1] == "Z":
                        poss_end_steps.append(step)

                    direction = path_instructions[step %
                                                  path_len]

                    interim_loc = path_map[interim_loc][0] if direction == "L" else path_map[interim_loc][1]
                    visited_locs.append(interim_loc)

                # print(loc, visited_locs)

                looping_locs_cache[loc] = (poss_end_steps, interim_loc)
                print('Cached', loc, len(looping_locs_cache))

            curr_ends.append(looping_locs_cache[loc])

        # print(curr_ends)
        common_ends = set(curr_ends[0][0])

        for i in range(1, len(curr_ends)):
            common_ends = common_ends.intersection(curr_ends[i][0])
            if len(common_ends) == 0:
                break

        if len(common_ends) > 0:
            return min(common_ends) + num_loops * path_len

        num_loops += 1
        locs = [l[1] for l in curr_ends]

        if all_cached:
            print('All cached')
            break

    # As all current elements are already cached, we must be in a loop
    # So now rather than caching within the inner loop, lets construct an outer loop
    outer_looping_locs_cache = {}
    core_looping_locs = locs.copy()

    loop_print_threshold = num_loops * path_len

    while True:

        # Ensure all locs are cached in outer_looping_locs_cache
        for loc in locs:
            if loc not in outer_looping_locs_cache:
                # Check if we can construct from existing cache
                within_loc_outer_loop = None
                for core_loc in core_looping_locs:
                    if core_loc not in outer_looping_locs_cache:
                        continue

                    if loc in outer_looping_locs_cache[core_loc][1]:
                        within_loc_outer_loop = core_loc
                        break

                if within_loc_outer_loop is not None:
                    core_loc_poss_end_steps, core_loc_elems = outer_looping_locs_cache[
                        within_loc_outer_loop]
                    curr_loc_index = core_loc_elems.index(loc)
                    curr_loc_outer_loop_elems = core_loc_elems[curr_loc_index:] + \
                        core_loc_elems[:curr_loc_index]
                    curr_loc_poss_steps = [(s - path_len * curr_loc_index) % (path_len * len(curr_loc_outer_loop_elems))
                                           for s in core_loc_poss_end_steps]
                    outer_looping_locs_cache[loc] = (
                        curr_loc_poss_steps, curr_loc_outer_loop_elems)
                else:
                    # Construct from scratch
                    curr_loc_loops = 0
                    interim_loc = loc
                    outer_loop_elems = []
                    outer_loop_poss_steps = []
                    while curr_loc_loops == 0 or interim_loc != loc:
                        outer_loop_elems.append(interim_loc)
                        curr_poss_end_steps, interim_loc = looping_locs_cache[interim_loc]
                        outer_loop_poss_steps.extend(
                            [s + curr_loc_loops * path_len for s in curr_poss_end_steps])
                        curr_loc_loops += 1

                    outer_looping_locs_cache[loc] = (
                        outer_loop_poss_steps, outer_loop_elems)

        curr_loc_outer_loops = {l: outer_looping_locs_cache[l] for l in locs}

        # Which loc has the smallest outer loop
        min_outer_loop_len, min_outer_loop_loc = min(
            (len(l[1][1]), l[0]) for l in curr_loc_outer_loops.items())

        outer_loop_common_end_steps = set(
            curr_loc_outer_loops[min_outer_loop_loc][1][0])

        some_in_common = True
        for other_loc in locs:
            if other_loc == min_outer_loop_loc:
                continue

            outer_loop_common_end_steps = outer_loop_common_end_steps.intersection(
                curr_loc_outer_loops[other_loc][0])
            if len(outer_loop_common_end_steps) == 0:
                some_in_common = False
                break

        if some_in_common:
            return min(outer_loop_common_end_steps) + num_loops * path_len

        locs = [l[1][min_outer_loop_len %
                     len(l[1])] for l in curr_loc_outer_loops.values()]
        num_loops += min_outer_loop_len

        curr_total_step_count = num_loops * path_len
        if curr_total_step_count > loop_print_threshold + 10000000000:
            print(time() - start, curr_total_step_count,
                  curr_total_step_count / 14631604759649)
            loop_print_threshold = curr_total_step_count


if __name__ == "__main__":
    test_sol = steps_to_reach("data1_test.txt")
    print(test_sol)
    assert test_sol == 6
    test_sol2 = steps_to_reach("data1_test2.txt")
    print(test_sol2)
    assert test_sol2 == 2
    test_sol3 = steps_to_reach("data2_test.txt")
    assert test_sol3 == 6
    print(test_sol3)
    print(steps_to_reach("data1_real.txt"))
