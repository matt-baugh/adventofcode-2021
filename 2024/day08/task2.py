from time import time

from utils.file_utils import load_file


def construct_map(content: list[str]):
    freq_map = {}
    for i, l in enumerate(content):
        for j, c in enumerate(l):
            if c != '.':
                if c not in freq_map:
                    freq_map[c] = []

                freq_map[c].append((i, j))

    return freq_map


def count_antinodes(filename_str: str) -> int:
    content = load_file(filename_str)

    num_rows = len(content)
    num_cols = len(content[0])

    freq_map = construct_map(content)

    antinode_locs = set()

    for c, n_list in freq_map.items():
        for i, (n1_i, n1_j) in enumerate(n_list):
            for n2_i, n2_j in n_list[i + 1:]:
                diff_i = n2_i - n1_i
                diff_j = n2_j - n1_j

                new_i = n2_i
                new_j = n2_j
                while new_i >= 0 and new_i < num_rows and new_j >= 0 and new_j < num_cols:
                    antinode_locs.add((new_i, new_j))
                    new_i += diff_i
                    new_j += diff_j

                new_i = n1_i
                new_j = n1_j
                while new_i >= 0 and new_i < num_rows and new_j >= 0 and new_j < num_cols:
                    antinode_locs.add((new_i, new_j))
                    new_i -= diff_i
                    new_j -= diff_j

                # for new_i, new_j in [(n2_i + diff_i, n2_j + diff_j), (n1_i - diff_i, n1_j - diff_j)]:

                #     if new_i >= 0 and new_i < num_rows and new_j >= 0 and new_j < num_cols:
                #         antinode_locs.add((new_i, new_j))

        # print(c)
        # print(len(antinode_locs), ':', antinode_locs)
        # print()

    return len(antinode_locs)


if __name__ == "__main__":

    print(count_antinodes("data1_test.txt"))
    start = time()
    print(count_antinodes("data1_real.txt"))
    print("Execution time:", time() - start)
