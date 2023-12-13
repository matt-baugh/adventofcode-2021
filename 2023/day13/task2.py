from pathlib import Path

from tqdm import tqdm

from utils.file_utils import load_file, chunk_input

PRINT = False

axis_multipliers = {
    0: 100,
    1: 1
}


def count_reflections(filename: str) -> int:
    all_input = load_file(Path(__file__).parent / filename)

    all_chunks = chunk_input(all_input, '', skip_empty=True)
    total = 0
    for c in tqdm(all_chunks):
        for a in range(2):
            curr_chunk = c if a == 1 else list(map(list, zip(*c)))
            axis_len = len(curr_chunk[0])
            possible_reflections = [(i, False) for i in range(axis_len - 1)]
            valid_reflections = []
            if PRINT:
                print('Axis:', a)
            for l in curr_chunk:
                for i, fixed_error in possible_reflections:
                    num_errors = sum(a != b for a, b in zip(l[i::-1], l[i + 1:]))
                    if num_errors == 0:
                        valid_reflections.append((i, fixed_error))
                    elif num_errors == 1 and not fixed_error:
                        valid_reflections.append((i, True))
                    else:
                        # Too many errors to correct, continue
                        continue
                
                if PRINT:
                    print(l)
                    print(valid_reflections)
                possible_reflections = valid_reflections
                valid_reflections = []

            total += sum((r + 1) * axis_multipliers[a]
                         for r, fixed_error in possible_reflections if fixed_error)

    return total


if __name__ == "__main__":
    test_sol = count_reflections("data1_test.txt")
    print(test_sol)
    assert test_sol == 400
    real_sol = count_reflections("data1_real.txt")
    print(real_sol)
    assert real_sol == 36735
