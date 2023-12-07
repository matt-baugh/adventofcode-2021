from collections import Counter
from pathlib import Path

from utils.file_utils import parse_file_lines

NUM_HAND_TYPES = 7

card_to_rank = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 0,
    "T": 10,
}


def rank_card(card: str) -> int:
    if card in card_to_rank:
        return card_to_rank[card]
    else:
        return int(card)


def calculate_total_winnings(filename: str) -> int:
    parsed_input = parse_file_lines(
        Path(__file__).parent / filename, split_val=None)

    hands_bids = [(h, int(b))for h, b in parsed_input]

    hand_groups = {i: [] for i in range(NUM_HAND_TYPES)}

    for h_b in hands_bids:
        curr_hand = h_b[0]

        card_to_counts = Counter(curr_hand)

        if card_to_counts["J"] > 0:
            if card_to_counts["J"] == 5:
                hand_groups[0].append(h_b)
                continue
            else:
                _, best_card = max((count, card) for card, count in card_to_counts.items() if card != "J")
                card_to_counts[best_card] += card_to_counts["J"]
                card_to_counts["J"] = 0

        counts_only = set(card_to_counts.values())

        max_count = max(counts_only)

        if max_count == 5:
            hand_groups[0].append(h_b)
        elif max_count == 4:
            hand_groups[1].append(h_b)
        elif max_count == 3:
            if 2 in counts_only:
                hand_groups[2].append(h_b)
            else:
                hand_groups[3].append(h_b)
        elif max_count == 2:
            count_counts = Counter(card_to_counts.values())
            if count_counts[2] == 2:
                hand_groups[4].append(h_b)
            else:
                hand_groups[5].append(h_b)
        else:
            # max_count == 1
            hand_groups[6].append(h_b)

    total_winnings = 0

    top_rank = len(hands_bids)
    for i in range(NUM_HAND_TYPES):
        hand_group = hand_groups[i]
        if len(hand_group) == 0:
            continue

        group_bottom_rank = top_rank - len(hand_group) + 1

        converted_hands = [([rank_card(c) for c in h], b) for h, b in hand_group]
        sorted_hands = sorted(converted_hands, key=lambda x: x[0])
        winnings = [(i + group_bottom_rank) * b for i,
                    (_, b) in enumerate(sorted_hands)]
        total_winnings += sum(winnings)
        top_rank = group_bottom_rank - 1

    assert top_rank == 0

    return total_winnings


if __name__ == "__main__":
    test_sol = calculate_total_winnings("data1_test.txt")
    print(test_sol)
    assert test_sol == 5905
    print(calculate_total_winnings("data1_real.txt"))
