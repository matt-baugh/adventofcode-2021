from time import time

from utils.file_utils import load_file


def compute_checksum(filename_str: str) -> int:
    content = load_file(filename_str)[0]
    # print(content, len(content))

    id_size_spaces = [[i, int(sz), int(sp)]
                      for i, (sz, sp) in enumerate(zip(content[::2], content[1::2]))]
    if len(content) % 2 == 1:
        id_size_spaces.append([len(id_size_spaces), int(content[-1]), 0])

    to_take_i = len(id_size_spaces) - 1
    defrag_list = []
    for i, sz, sp in id_size_spaces:
        if i > to_take_i:
            break

        if sz > 0:
            defrag_list.append((i, sz))

        if i == to_take_i:
            break

        while sp > 0:
            while id_size_spaces[to_take_i][1] == 0:
                to_take_i -= 1

            if to_take_i <= i:
                break

            to_take_sz = min(sp, id_size_spaces[to_take_i][1])

            defrag_list.append((to_take_i, to_take_sz))
            id_size_spaces[to_take_i][1] -= to_take_sz
            sp -= to_take_sz

    checksum = 0
    curr_mem_loc = 0
    for i, (mem_id, sz) in enumerate(defrag_list):
        if mem_id != 0:
            r = list(range(curr_mem_loc * mem_id,
                           (curr_mem_loc + sz) * mem_id, mem_id))
            checksum += sum(r)
        curr_mem_loc += sz

    return checksum


if __name__ == "__main__":

    print(compute_checksum("data1_test.txt"))
    start = time()
    print(compute_checksum("data1_real.txt"))
    print("Execution time:", time() - start)
