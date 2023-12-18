from day18.task1 import calc_lagoon_size, UP, DOWN, LEFT, RIGHT

dir_map = {
    '0': RIGHT,
    '1': DOWN,
    '2': LEFT,
    '3': UP
}

def complex_intr_decode(instr_list):
    hex_code = instr_list[2][2:-1]
    return dir_map[hex_code[-1]], int(hex_code[:-1], 16)

if __name__ == "__main__":
    test_sol = calc_lagoon_size("data1_test.txt", complex_intr_decode)
    print(test_sol)
    assert test_sol == 952408144115
    real_sol = calc_lagoon_size("data1_real.txt", complex_intr_decode)
    print(real_sol)
    assert real_sol == 60612092439765