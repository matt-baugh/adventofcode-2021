from pathlib import Path

import numpy as np

from utils.file_utils import parse_file_lines

PRINT = False


def calc_max_group_sizes(filename: str) -> int:
    raw_input = parse_file_lines(
        Path(__file__).parent / filename, (': ', (None, None)), skip_empty=True)

    # print(raw_input)
    graph = {}
    for ((from_n,), to_ns) in raw_input:
        graph.setdefault(from_n, set()).update(to_ns)
        for t_n in to_ns:
            graph.setdefault(t_n, set()).add(from_n)
    
    print(graph)
    return 0

if __name__ == "__main__":
    test_sol = calc_max_group_sizes("data1_test.txt")
    print(test_sol)
    assert test_sol == 54
    real_sol = calc_max_group_sizes("data1_real.txt")
    print(real_sol)
    # assert real_sol == 24192
