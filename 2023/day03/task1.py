from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation

from utils.file_utils import load_file


def check_engine(filename: str):    
    input_str = load_file(Path(__file__).parent / filename)

    all_input = np.array([[c for c in l] for l in input_str])

    all_int = np.array([[c.isdigit() for c in l] for l in input_str])
    all_symbol = (all_input != '.') & ~all_int

    symbol_adjacent = binary_dilation(all_symbol, structure=np.ones((3, 3)))
    int_adjacent = all_int & symbol_adjacent
    
    total = 0
    
    for i, line in enumerate(all_input):
        
        digit_mask = all_int[i]
        symbol_neigbour = int_adjacent[i]
        
        if not np.any(symbol_neigbour):
            continue
        
        whole_number_neighbour = binary_dilation(symbol_neigbour, mask=digit_mask, iterations=0)
        
        filtered_line = ''.join(np.where(whole_number_neighbour, line, ' '))
        nums = [int(n) for n in filtered_line.split() if n.isdigit()]
        total += sum(nums)
    

    return total


if __name__ == "__main__":
    print(check_engine("data1_test.txt"))
    print(check_engine("data1_real.txt"))
