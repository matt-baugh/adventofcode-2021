from time import time

from utils.file_utils import load_file, chunk_input


def construct_rules(rule_inputs: list[str]) -> dict[int, list[int]]:

    rules = {}
    for rule in rule_inputs:
        num_before, num_after = rule.split("|")
        num_before = int(num_before)
        num_after = int(num_after)
        if num_before not in rules:
            rules[num_before] = {num_after}
        else:
            rules[num_before].add(num_after)
    return rules


def sum_invalid_middle_pages(filename_str: str) -> int:

    content = load_file(filename_str)

    rule_inputs, pages_inputs = chunk_input(content, "")

    rules = construct_rules(rule_inputs)

    middle_page_sum = 0

    for pages in pages_inputs:
        pages = list(map(int, pages.split(',')))
        left_pages = set()
        valid = True
        for p in pages:
            if p in rules:
                if left_pages.intersection(rules[p]):
                    valid = False
                    break

            left_pages.add(p)

        if not valid:
            pages_set = set(pages)

            page_and_before = []

            for p in pages:
                if p in rules:
                    page_and_before.append(
                        (p, len(set(rules[p]).intersection(pages_set))))
                else:
                    page_and_before.append((p, 0))

            page_and_before.sort(key=lambda x: x[1], reverse=True)
            middle_page_sum += page_and_before[len(page_and_before) // 2][0]

        # print()

    return middle_page_sum


if __name__ == "__main__":

    print(sum_invalid_middle_pages("data1_test.txt"))
    start = time()
    print(sum_invalid_middle_pages("data1_real.txt"))
    print("Execution time:", time() - start)
