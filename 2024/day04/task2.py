from time import time

from utils.file_utils import load_file


step_dirs = [

]


def count_xmas(filename_str: str) -> int:
    content = load_file(filename_str, (":", (None, " ")))

    num_rows = len(content)
    num_cols = len(content[0])

    # print(num_rows, num_cols)
    # print(content)

    count = 0
    for i in range(1, num_rows - 1):
        for j in range(1, num_cols - 1):
            if content[i][j] == "A":
                top_left = content[i - 1][j - 1]
                top_right = content[i - 1][j + 1]
                bot_left = content[i + 1][j - 1]
                bot_right = content[i + 1][j + 1]
                if top_left == "M":
                    if top_right == "M":
                        if bot_left == "S" and bot_right == "S":
                            count += 1
                    elif bot_left == "M":
                        if top_right == "S" and bot_right == "S":
                            count += 1

                elif top_left == "S":
                    if top_right == "S":
                        if bot_left == "M" and bot_right == "M":
                            count += 1
                    elif bot_left == "S":
                        if top_right == "M" and bot_right == "M":
                            count += 1

    return count


if __name__ == "__main__":

    print(count_xmas("data1_test.txt"))
    start = time()
    print(count_xmas("data1_real.txt"))
    print("Execution time:", time() - start)
