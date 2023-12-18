from dataclasses import dataclass
from pathlib import Path


from utils.file_utils import parse_file_lines

PRINT = False

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'


@dataclass
class Edge:
    start: tuple[int, int]
    end: tuple[int, int]
    dig_dir: str
    prev_edge: 'Edge'
    next_edge: 'Edge' = None
    c1: tuple[float, float] = None
    c2: tuple[float, float] = None


def calc_lagoon_size(filename: str, get_dir_amount) -> int:

    raw_input = parse_file_lines(Path(__file__).parent / filename)
    all_edges = []
    curr_coord = (0, 0)
    last_edge = None
    for instr_list in raw_input:
        d, amount = get_dir_amount(instr_list)

        if d == UP:
            new_coord = (curr_coord[0] - amount, curr_coord[1])
        elif d == DOWN:
            new_coord = (curr_coord[0] + amount, curr_coord[1])
        elif d == LEFT:
            new_coord = (curr_coord[0], curr_coord[1] - amount)
        elif d == RIGHT:
            new_coord = (curr_coord[0], curr_coord[1] + amount)

        new_edge = Edge(curr_coord, new_coord, d, last_edge)
        if last_edge:
            last_edge.next_edge = new_edge

        all_edges.append(new_edge)
        last_edge = new_edge
        curr_coord = new_coord

    assert curr_coord == (0, 0)
    assert all_edges[0].prev_edge is None
    assert all_edges[-1].next_edge is None
    all_edges[0].prev_edge = all_edges[-1]
    all_edges[-1].next_edge = all_edges[0]

    for e in all_edges:
        if e.dig_dir == UP:
            assert e.prev_edge.dig_dir == LEFT or e.prev_edge.dig_dir == RIGHT
            if e.prev_edge.dig_dir == LEFT:
                e.c1 = (e.start[0] + 0.5, e.start[1] - 0.5)
                e.c2 = (e.start[0] - 0.5, e.end[1] + 0.5)
            else:
                e.c1 = (e.start[0] - 0.5, e.start[1] - 0.5)
                e.c2 = (e.start[0] + 0.5, e.end[1] + 0.5)
        elif e.dig_dir == DOWN:
            assert e.prev_edge.dig_dir == LEFT or e.prev_edge.dig_dir == RIGHT
            if e.prev_edge.dig_dir == LEFT:
                e.c1 = (e.start[0] + 0.5, e.start[1] + 0.5)
                e.c2 = (e.start[0] - 0.5, e.end[1] - 0.5)
            else:
                e.c1 = (e.start[0] - 0.5, e.start[1] + 0.5)
                e.c2 = (e.start[0] + 0.5, e.end[1] - 0.5)
        elif e.dig_dir == LEFT:
            assert e.prev_edge.dig_dir == UP or e.prev_edge.dig_dir == DOWN
            if e.prev_edge.dig_dir == UP:
                e.c1 = (e.start[0] + 0.5, e.start[1] - 0.5)
                e.c2 = (e.end[0] - 0.5, e.start[1] + 0.5)
            else:
                e.c1 = (e.start[0] + 0.5, e.start[1] + 0.5)
                e.c2 = (e.end[0] - 0.5, e.start[1] - 0.5)
        elif e.dig_dir == RIGHT:
            assert e.prev_edge.dig_dir == UP or e.prev_edge.dig_dir == DOWN
            if e.prev_edge.dig_dir == UP:
                e.c1 = (e.start[0] - 0.5, e.start[1] - 0.5)
                e.c2 = (e.end[0] + 0.5, e.start[1] + 0.5)
            else:
                e.c1 = (e.start[0] - 0.5, e.start[1] + 0.5)
                e.c2 = (e.end[0] + 0.5, e.start[1] - 0.5)

    area_1 = 0
    area_2 = 0
    for e in all_edges:

        area_1 += 0.5 * (e.c1[0] + e.next_edge.c1[0]) * \
            (e.c1[1] - e.next_edge.c1[1])
        area_2 += 0.5 * (e.c2[0] + e.next_edge.c2[0]) * \
            (e.c2[1] - e.next_edge.c2[1])
        if PRINT:
            print(area_1, area_2)

    return max(abs(area_1), abs(area_2))


def basic_intr_decode(instr_list):
    return (instr_list[0], int(instr_list[1]))


if __name__ == "__main__":
    test_sol = calc_lagoon_size("data1_test.txt", basic_intr_decode)
    print(test_sol)
    assert test_sol == 62
    real_sol = calc_lagoon_size("data1_real.txt", basic_intr_decode)
    print(real_sol)
    assert real_sol == 52035
