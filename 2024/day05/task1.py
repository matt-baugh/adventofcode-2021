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


def sum_valid_middle_pages(filename_str: str) -> int:

    content = load_file(filename_str)

    rule_inputs, pages_inputs = chunk_input(content, "")

    rules = construct_rules(rule_inputs)

    middle_page_sum = 0

    print(rules)

    for pages in pages_inputs:
        pages = list(map(int, pages.split(',')))
        left_pages = set()
        valid = True
        for p in pages:
            if p in rules:
                if left_pages.intersection(rules[p]):
                    valid = False
                    # print("Invalid", pages, ' at ', p)
                    break

            left_pages.add(p)
        if valid:
            middle_page_sum += pages[len(pages) // 2]
            # print(pages, pages[len(pages) // 2])

    return middle_page_sum


if __name__ == "__main__":

    print(sum_valid_middle_pages("data1_test.txt"))
    # start = time()
    # print(sum_valid_middle_pages("data1_real.txt"))
    # print("Execution time:", time() - start)
