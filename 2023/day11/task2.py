from day11.task1 import sum_shortest_paths

if __name__ == "__main__":
    test_sol = sum_shortest_paths("data1_test.txt", 10)
    print(test_sol)
    assert test_sol == 1030
    test_sol = sum_shortest_paths("data1_test.txt", 100)
    print(test_sol)
    assert test_sol == 8410
    print(sum_shortest_paths("data1_real.txt", 1000000))
