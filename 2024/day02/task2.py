from utils.file_utils import load_file


def check_safe(ints: list[int]) -> bool:
    if ints[1] > ints[0]:
        decreasing = False
    elif ints[1] < ints[0]:
        decreasing = True
    else:
        return False

    i1 = ints[0]
    for i2 in ints[1:]:
        if decreasing:
            if i2 >= i1 or (i1 - i2) > 3:
                return False

        else:
            if i2 <= i1 or (i2 - i1) > 3:
                return False

        i1 = i2

    return True


def count_safe(filename_str: str, allow_fail=False) -> int:
    content = [[int(i) for i in l.split()] for l in load_file(filename_str)]

    safe = 0
    for l in content:
        if len(l) == 1:
            safe += 1
            continue
        is_safe = False
        for i in range(len(l)):
            if check_safe(l[:max(i, 0)]  + l[i + 1:]):
                is_safe = True
                break
        
        if is_safe:
            safe += 1
            # print(l)
    return safe


if __name__ == "__main__":
    print(count_safe("data1_test.txt", True))
    print(count_safe("data1_real.txt", True))
