from time import time

from utils.file_utils import load_file


step_dirs = [(h, v) for h in range(-1, 2)
             for v in range(-1, 2) if not (h == 0 and v == 0)]


def count_xmas(filename_str: str) -> int:
    content = load_file(filename_str, (":", (None, " ")))

    num_rows = len(content)
    num_cols = len(content[0])

    # print(num_rows, num_cols)
    # print(content)

    count = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if content[i][j] == "X":
                for h_dir, v_dir in step_dirs:
                    curr_i = i
                    curr_j = j
                    found = False
                    for l in "MAS":
                        curr_i += h_dir
                        curr_j += v_dir
                        if curr_i < 0 or curr_i >= num_rows or curr_j < 0 or curr_j >= num_cols:
                            break
                        if content[curr_i][curr_j] != l:
                            break
                        if l == "S":
                            found = True
                    if found:
                        count += 1

    return count


if __name__ == "__main__":

    print(count_xmas("data1_test.txt"))
    start = time()
    print(count_xmas("data1_real.txt"))
    print("Execution time:", time() - start)
