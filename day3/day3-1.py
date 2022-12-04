from distutils.command.clean import clean
import sys, os
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


class Rucksack:
    def __init__(self, line):
        clean_line = line.strip()
        num_items = len(clean_line)

        half_num_items = num_items // 2

        comp0_sorted = "".join(sorted(clean_line[0:half_num_items]))
        comp1_sorted = "".join(sorted(clean_line[half_num_items:num_items]))

        self.compartments = [comp0_sorted, comp1_sorted]

    def get_common_item(self):
        for item_0 in self.compartments[0]:
            i_item = binary_search(self.compartments[1], item_0)

            if i_item >= 0:
                return item_0
        
        return None





def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    rucksacks = [Rucksack(line) for line in lines]
    common_items = tuple(rucksack.get_common_item() for rucksack in rucksacks)

    total_priority_of_common_items = sum(get_item_priority(item) for item in common_items)

    print("total priority: {priority}".format(priority = total_priority_of_common_items))

    
if __name__ == "__main__":
    main()