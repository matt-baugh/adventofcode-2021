from utils.file_utils import load_file


def check_safe(ints: list[int], allow_fail: bool = False) -> bool:
    if ints[1] > ints[0]:
        decreasing = False
    elif ints[1] < ints[0]:
        decreasing = True
    else:
        return False

    used_skip = False
    i1 = ints[0]
    for i2 in ints[1:]:
        if decreasing:
            if i2 >= i1 or (i1 - i2) > 3:
                if allow_fail and not used_skip:
                    used_skip = True
                else:

                    return False
            else:
                i1 = i2
        else:
            if i2 <= i1 or (i2 - i1) > 3:
                if allow_fail and not used_skip:
                    used_skip = True
                else:
                    return False
            else:
                i1 = i2

    return True


def count_safe(filename_str: str, allow_fail=False) -> int:
    content = [[int(i) for i in l.split()] for l in load_file(filename_str)]

    return sum(check_safe(l, allow_fail) for l in content)


if __name__ == "__main__":
    print(count_safe("data1_test.txt"))
    print(count_safe("data1_real.txt"))
    print(count_safe("data1_test.txt", True))
    print(count_safe("data1_real.txt", True))
