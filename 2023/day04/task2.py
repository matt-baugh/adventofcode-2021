from pathlib import Path

from utils.file_utils import parse_file_lines


def sum_scratch_points(filename: str):    
    parsed_input = parse_file_lines(Path(__file__).parent / filename, split_val=(':', (None, ('|', (None, None)))))

    card_count = [1] * len(parsed_input)

    total = 0
    for (_, game_id), (win_nums, my_nums) in parsed_input[::-1]:
        game_id = int(game_id) - 1
        num_matches = len(set(win_nums).intersection(set(my_nums)))

        for i in range(1, num_matches + 1):
            if game_id + i < len(card_count):
                card_count[game_id] += card_count[game_id + i]

        total += card_count[game_id]

    return total


if __name__ == "__main__":
    print(sum_scratch_points("data1_test.txt"))
    print(sum_scratch_points("data1_real.txt"))
