from utils.file_utils import load_file, split_str


def sum_distances(filename: str) -> int:
    content = [[int(i) for i in split_str(l, "   ")] for l in load_file(filename)]
    l1, l2 = [list(li) for li in zip(*content)]

    l1.sort()
    l2.sort()

    return sum([abs(l1[i] - l2[i]) for i in range(len(l1))])

if __name__ == "__main__":
    # print(sum_distances("data1_test.txt"))
    print(sum_distances("data_real.txt"))
