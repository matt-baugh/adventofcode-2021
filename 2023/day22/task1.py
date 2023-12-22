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
    supporting_record: dict[int, list[int]] = {}
    # Dictionary of block id -> list of block ids that support it
    supported_record: dict[int, list[int]] = {}

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
        below_blocks = set([b for h, b in pos_heights if h == max_height])
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

    num_removable = 0
    for block_id, supporting_blocks in supporting_record.items():
        if all(len(supported_record[b]) > 1 for b in supporting_blocks):
            num_removable += 1

    return num_removable


if __name__ == "__main__":
    test_sol = calc_possible_remove("data1_test.txt")
    print(test_sol)
    assert test_sol == 5
    real_sol = calc_possible_remove("data1_real.txt")
    print(real_sol)
    assert real_sol == 524
