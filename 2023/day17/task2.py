from day17.task1 import calc_heat_loss


if __name__ == "__main__":
    test_sol = calc_heat_loss("data1_test.txt", 4, 10)
    print(test_sol)
    assert test_sol == 94
    real_sol = calc_heat_loss("data1_real.txt", 4, 10)
    print(real_sol)
    assert real_sol == 1367
