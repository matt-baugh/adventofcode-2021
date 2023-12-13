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
            possible_reflections = list(range(axis_len - 1))
            valid_reflections = []
            for l in curr_chunk:
                for i in possible_reflections:
                    if all(a == b for a, b in zip(l[i::-1], l[i + 1:])):
                        valid_reflections.append(i)

                possible_reflections = valid_reflections
                valid_reflections = []

            total += sum((r + 1) * axis_multipliers[a]
                         for r in possible_reflections)

    return total


if __name__ == "__main__":
    test_sol = count_reflections("data1_test.txt")
    print(test_sol)
    assert test_sol == 405
    real_sol = count_reflections("data1_real.txt")
    print(real_sol)
    # assert real_sol == 6935
