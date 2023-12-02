from pathlib import Path

import numpy as np

from utils.file_utils import load_file


def check_games(filename: str):
    total = 0

    for line in load_file(Path(__file__).parent / filename):
        game_descr, hands = line.split(":")

        _, game_id = game_descr.split(" ")
        game_id = int(game_id)

        min_poss_counts = {}

        possible = True
        for hand in hands.split(';'):

            for group in hand.split(","):
                sects = group.split(" ")

                assert sects[1].isdigit()
                num = int(sects[1])
                colour = sects[2]

                assert colour in ["blue", "red", "green"], 'Invalid colour: {}'

                if colour not in min_poss_counts:
                    min_poss_counts[colour] = num
                else:
                    min_poss_counts[colour] = max(min_poss_counts[colour], num)

        total += np.prod(list(min_poss_counts.values()))

    return total


if __name__ == "__main__":
    print(check_games("data1_test.txt"))
    print(check_games("data1_real.txt"))
