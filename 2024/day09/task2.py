from time import time
import bisect

from utils.file_utils import load_file


def compute_checksum(filename_str: str) -> int:
    content = load_file(filename_str)[0]
    # print(content, len(content))

    id_size_spaces = []
    max_space = 0
    space_dict = {}

    for file_id, (sz, sp) in enumerate(zip(content[::2], content[1::2])):
        sp = int(sp)
        id_size_spaces.append([file_id, int(sz), sp, [], True])
        if sp > max_space:
            max_space = sp

        if sp not in space_dict:
            space_dict[sp] = []
        space_dict[sp].append(file_id)

    if len(content) % 2 == 1:
        id_size_spaces.append(
            [len(id_size_spaces), int(content[-1]), 0, [], True])

    for file_id in reversed(range(len(id_size_spaces))):
        file_id, sz, sp, _, file_present = id_size_spaces[file_id]
        if sz == 0 or not file_present:
            continue
        best_loc = None
        best_loc_sp = None
        for poss_space in range(sz, max_space + 1):
            if poss_space in space_dict and len(space_dict[poss_space]) > 0 and (best_loc is None or space_dict[poss_space][0] < best_loc):
                best_loc = space_dict[poss_space][0]
                best_loc_sp = poss_space

        if best_loc is not None and best_loc < file_id:

            assert best_loc_sp is not None and best_loc_sp >= sz

            id_size_spaces[best_loc][3].append((file_id, sz))
            space_dict[best_loc_sp] = space_dict[best_loc_sp][1:]

            remaining_space = best_loc_sp - sz
            id_size_spaces[best_loc][2] = remaining_space
            if remaining_space > 0:
                if remaining_space not in space_dict:
                    space_dict[remaining_space] = []

                bisect.insort(space_dict[remaining_space], best_loc)

            id_size_spaces[file_id][4] = False

    checksum = 0
    curr_mem_loc = 0
    for file_id, sz, sp, moved_ones, file_present in id_size_spaces:

        if file_present:
            moved_ones = [(file_id, sz)] + moved_ones
        else:
            curr_mem_loc += sz

        for mem_id, sz in moved_ones:
            if mem_id != 0:
                r = list(range(curr_mem_loc * mem_id,
                               (curr_mem_loc + sz) * mem_id, mem_id))
                checksum += sum(r)
            curr_mem_loc += sz

            # print(mem_id, sz, checksum, curr_mem_loc)

        curr_mem_loc += sp
        # print(curr_mem_loc)

    return checksum


if __name__ == "__main__":

    print(compute_checksum("data1_test.txt"))
    start = time()
    print(compute_checksum("data1_real.txt"))
    print("Execution time:", time() - start)
