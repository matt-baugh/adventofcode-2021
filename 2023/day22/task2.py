from pathlib import Path

from utils.file_utils import parse_file_lines

PRINT = False


def calc_possible_remove(filename: str) -> int:
    # each line is pair of coordinates (x, y, z)
    init_input = parse_file_lines(
        Path(__file__).parent / filename, ("~", (',', ',')))

    init_input = list(sorted(tuple(sorted([tuple(map(int, c[::-1])) for c in b]))
                             for b in init_input))

    # Dictionary of i pos -> j pos -> (height, block id)
    highest_positions: dict[int, dict[int, tuple[int, int]]] = {}

    # Dictionary of block id -> list of block ids that it supports
    supporting_record: dict[int, set[int]] = {}
    # Dictionary of block id -> list of block ids that support it
    supported_record: dict[int, set[int]] = {}
    block_final_heights = []

    for block_id, ((c1_z, c1_i, c1_j), (c2_z, c2_i, c2_j)) in enumerate(init_input):
        assert c1_z <= c2_z
        assert c1_i <= c2_i
        assert c1_j <= c2_j

        spatial_coords = [(i, j) for i in range(c1_i, c2_i + 1)
                          for j in range(c1_j, c2_j + 1)]
        block_height = c2_z - c1_z + 1

        # Find heights at each position
        pos_heights = [highest_positions.get(i, {}).get(
            j, (0, 'floor')) for i, j in spatial_coords]
        max_height = max(h for h, _ in pos_heights)
        below_blocks = set(b for h, b in pos_heights if h == max_height)
        below_blocks.discard('floor')

        for (i, j) in spatial_coords:

            if i not in highest_positions:
                highest_positions[i] = {}

            # Could use setdefault?
            highest_positions[i][j] = (max_height + block_height, block_id)

        supported_record[block_id] = below_blocks
        for b in below_blocks:
            supporting_record[b].add(block_id)

        supporting_record[block_id] = set()
        block_final_heights.append((block_id, max_height + block_height))

    blocks_top_to_bottom = sorted(
        block_final_heights, key=lambda x: x[1], reverse=True)

    total_falling = 0
    # dict of block id -> (set of blocks that have already fallen, set of blocks that may be unstable if this block falls)
    remove_results = {}
    for block_id, _ in blocks_top_to_bottom:
        connected_blocks = supporting_record[block_id]

        if len(connected_blocks) == 0:
            remove_results[block_id] = (set(), set(), set())

        # Compute result of removing current block
        curr_unstable = set()  # Blocks which may fall
        curr_fallen = set()  # Blocks which definitely fall
        curr_stable_despite_remove = set()  # Blocks which definitely don't fall
        curr_stable_adj = set()  # Blocks which are stable despite removal of adjacent blocks
        remain_stable = connected_blocks.copy()
        for b in connected_blocks:
            if len(supported_record[b]) == 1:
                curr_fallen.add(b)
                curr_fallen |= remove_results[b][0]
                curr_unstable |= remove_results[b][1]
            else:
                curr_stable_adj.add(b)
                curr_stable_despite_remove.add(b)
                curr_stable_despite_remove |= remove_results[b][2]
            remain_stable |= remove_results[b][2]

        curr_unstable -= curr_stable_despite_remove
        removed_a_block = True
        while removed_a_block:
            removed_a_block = False
            next_unstable = set()
            for b in curr_unstable:
                if len(supported_record[b] - curr_fallen) == 0:
                    curr_fallen.add(b)
                    curr_fallen |= remove_results[b][0]
                    next_unstable |= remove_results[b][1]
                    removed_a_block = True
                else:
                    next_unstable.add(b)
            curr_unstable = next_unstable

        remove_results[block_id] = (curr_fallen, curr_unstable | curr_stable_adj, remain_stable)
        total_falling += len(curr_fallen)

    return total_falling


if __name__ == "__main__":
    test_sol = calc_possible_remove("data1_test.txt")
    print(test_sol)
    assert test_sol == 7
    real_sol = calc_possible_remove("data1_real.txt")
    print(real_sol)
    assert real_sol == 77070
