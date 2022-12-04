import sys, os
from tokenize import group
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

s = ''

# unicode code points for latin A-Z are sequential
def is_uppercase_char(char):
    return ord(char) >= ord("A") and ord(char) <= ord("Z")

# unicode code points for latin a-z are sequential
def is_lowercase_char(char):
    return ord(char) >= ord("a") and ord(char) <= ord("z")


def get_item_priority(item):
    if is_uppercase_char(item):
        return ord(item) - ord("A") + 27
    elif is_lowercase_char(item):
        return ord(item) - ord("a") + 1

def binary_search(items, item):
    low = 0
    high = len(items) - 1

    # Repeat until the pointers low and high meet each other
    while low <= high:

        mid = low + (high - low)//2

        if items[mid] == item:
            return mid

        elif items[mid] < item:
            low = mid + 1

        else:
            high = mid - 1

    return -1


def get_common_items_in_compartments(compartments_with_sorted_items = []):

    # sort by compartment length so we have the fewest # number of iterations
    sorted_compartments = sorted(compartments_with_sorted_items, key=len)

    other_comps = sorted_compartments[1:]

    # todo: use the priority of the item to exclude iterations

    for item in sorted_compartments[0]:
        found = True
        for comp in other_comps:
            if binary_search(comp, item) < 0:
                found = False
                break
        
        if found:
            return item
    
    return None
   


class Rucksack:
    def __init__(self, line):
        clean_line = line.strip()
        num_items = len(clean_line)

        half_num_items = num_items // 2

        comp0_sorted = "".join(sorted(clean_line[0:half_num_items]))
        comp1_sorted = "".join(sorted(clean_line[half_num_items:num_items]))

        self.all_items_sorted = "".join(sorted(clean_line))

        self.compartments = [comp0_sorted, comp1_sorted]

    def get_common_item(self):
        return get_common_items_in_compartments(self.compartments)






def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    rucksacks = tuple(Rucksack(line) for line in lines)

    rucksack_iter = iter(rucksacks)

    rucksack_groups = tuple((r1,r2,r3) for r1,r2,r3 in zip(rucksack_iter, rucksack_iter, rucksack_iter) )

    sack_item_groups = []

    for g in rucksack_groups:
        sack_item_groups.append([r.all_items_sorted for r in g])
        

    #common_items = tuple(rucksack.get_common_item() for rucksack in rucksacks)

    common_items = tuple(get_common_items_in_compartments(sack_item_group) for sack_item_group in sack_item_groups)

    total_priority_of_common_items = sum(get_item_priority(item) for item in common_items)

    print("total priority: {priority}".format(priority = total_priority_of_common_items))

    
if __name__ == "__main__":
    main()