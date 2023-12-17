from pathlib import Path

from utils.file_utils import load_file

PRINT = False

VERT_SPLIT = '|'
HOR_SPLIT = '-'
DIAG_1 = '/'
DIAG_2 = '\\'

MIRROR_CHARS = [VERT_SPLIT, HOR_SPLIT, DIAG_1, DIAG_2]

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


MIRROR_DIR_CHANGE = {
    VERT_SPLIT: {
        NORTH: (NORTH,),
        EAST: (NORTH, SOUTH),
        SOUTH: (SOUTH,),
        WEST: (NORTH, SOUTH),
    },
    HOR_SPLIT: {
        NORTH: (EAST, WEST),
        EAST: (EAST,),
        SOUTH: (EAST, WEST),
        WEST: (WEST,),
    },
    DIAG_1: {
        NORTH: (EAST,),
        EAST: (NORTH,),
        SOUTH: (WEST,),
        WEST: (SOUTH,),
    },
    DIAG_2: {
        NORTH: (WEST,),
        EAST: (SOUTH,),
        SOUTH: (EAST,),
        WEST: (NORTH,),
    },
}


def calc_energy(filename: str) -> int:
    raw_input = load_file(Path(__file__).parent / filename)

    all_mirrors = []
    for i, r in enumerate(raw_input):
        for j, c in enumerate(r):
            if c in MIRROR_CHARS:
                all_mirrors.append(((i, j), c))

    input_shape = (len(raw_input), len(raw_input[0]))

    return calc_energy_from(((0, 0), EAST), all_mirrors, input_shape)


def calc_energy_from(initial_beam, all_mirrors, input_shape):

    energised_map = [[False] * input_shape[1] for _ in range(input_shape[0])]
    assert sum(sum(row) for row in energised_map) == 0

    mirrors_at_start = [m for m in all_mirrors if m[0] == initial_beam[0]]
    if len(mirrors_at_start) > 0:
        assert len(mirrors_at_start) == 1
        curr_beams = [(initial_beam[0], d)
                      for d in MIRROR_DIR_CHANGE[mirrors_at_start[0][1]][initial_beam[1]]]

        initial_beam = (
            initial_beam[0], MIRROR_DIR_CHANGE[mirrors_at_start[0][1]][initial_beam[1]][0])
    else:
        curr_beams = [initial_beam]
    all_beams = set(curr_beams)

    while len(curr_beams) > 0:
        new_beams = []
        for (start_coord, dir) in curr_beams:
            axis = 0 if dir in (NORTH, SOUTH) else 1
            if PRINT:
                print(start_coord, dir, axis)
            poss_mirrors = [m for m in all_mirrors if m[0]
                            [1 - axis] == start_coord[1 - axis]]
            mirror_hit = None
            if dir in (NORTH, WEST):
                poss_mirrors = [m for m in poss_mirrors if m[0]
                                [axis] < start_coord[axis]]

                if len(poss_mirrors) == 0:
                    end = tuple(-1 if i ==
                                axis else start_coord[i] for i in range(2))
                else:
                    mirror_hit = max(
                        poss_mirrors, key=lambda m: m[0][axis])
                    end = mirror_hit[0]
            else:
                poss_mirrors = [m for m in poss_mirrors if m[0]
                                [axis] > start_coord[axis]]

                if len(poss_mirrors) == 0:
                    end = tuple(input_shape[0] if i ==
                                axis else start_coord[i] for i in range(2))
                else:
                    mirror_hit = min(
                        poss_mirrors, key=lambda m: m[0][axis])
                    end = mirror_hit[0]

            assert end != start_coord, (start_coord, dir, poss_mirrors)
            step = 1 if end > start_coord else -1
            for a_i in range(start_coord[axis], end[axis], step):
                a = tuple(a_i if i ==
                          axis else start_coord[1 - axis] for i in range(2))
                energised_map[a[0]][a[1]] = True

            if mirror_hit is not None:
                if PRINT:
                    print("Mirror hit:", mirror_hit)
                new_dirs = MIRROR_DIR_CHANGE[mirror_hit[1]][dir]
                for d in new_dirs:
                    poss_beam = (mirror_hit[0], d)
                    if poss_beam not in all_beams:
                        all_beams.add(poss_beam)
                        new_beams.append((mirror_hit[0], d))

        if PRINT:
            print("New beams:")
            for b in new_beams:
                print(b)
            for r in energised_map:
                print("".join("#" if c else "." for c in r))
            print()
        curr_beams = new_beams

    return sum(sum(row) for row in energised_map)


if __name__ == "__main__":
    test_sol = calc_energy("data1_test.txt")
    print(test_sol)
    assert test_sol == 46
    real_sol = calc_energy("data1_real.txt")
    print(real_sol)
    assert real_sol == 7884
