from pathlib import Path

import numpy as np
from scipy.ndimage import label

from utils.file_utils import load_file
from time import time

def check_engine(filename: str):    
    input_str = load_file(Path(__file__).parent / filename)

    all_input = np.array([[c for c in l] for l in input_str])

    all_int = np.array([[c.isdigit() for c in l] for l in input_str])
    all_stars = all_input == '*'

    labelled_nums = label(all_int, structure=np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]))[0]

    total = 0
    for gear_coord in np.argwhere(all_stars):
        gear_neighbours = tuple(slice(max(c-1, 0), c +2) for c in gear_coord)

        gear_neighbour_labels = np.unique(labelled_nums[gear_neighbours])
        
        assert gear_neighbour_labels[0] == 0, 'Gear should not be adjacent to a number'
        
        if len(gear_neighbour_labels) == 3:
            good_neighbour_labels = gear_neighbour_labels[1:]
            neibouring_rows_vals = all_input[gear_neighbours[0]]
            neigbouring_rows_labels = labelled_nums[gear_neighbours[0]]
            total += np.prod([int(''.join(neibouring_rows_vals[np.nonzero(neigbouring_rows_labels == l)])) for l in good_neighbour_labels])
    return total


if __name__ == "__main__":
    start = time()
    test_res = check_engine("data1_test.txt")
    assert test_res == 467835
    print(test_res)
    real_res = check_engine("data1_real.txt")
    assert real_res == 75220503
    print(real_res)
    
    print(f"Total time: {time() - start}")

