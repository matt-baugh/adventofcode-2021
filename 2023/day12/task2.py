from day12.task1 import sum_possible_arrangements



if __name__ == "__main__":
    test_sol = sum_possible_arrangements("data1_test.txt", 5)
    print(test_sol)
    assert test_sol == 525152
    print(sum_possible_arrangements("data1_real.txt", 5))
