from utils.file_utils import load_file, split_str
from collections import Counter

def sum_distances(filename: str) -> int:
    content = [[int(i) for i in split_str(l, "   ")] for l in load_file(filename)]
    l1, l2 = [list(li) for li in zip(*content)]

    l2_counts = Counter(l2)
    
    return sum(i * l2_counts[i] for i in l1)
if __name__ == "__main__":
    print(sum_distances("data1_test.txt"))
    print(sum_distances("data_real.txt"))
