import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines


def compare_input_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1

    if isinstance(left, list) and not isinstance(right, list):
        return compare_input_order(left, [right])

    if not isinstance(left, list) and isinstance(right, list):
        return compare_input_order([left], right)
    
    for i_l in range(len(left)):

        right_is_out_of_items = i_l >= len(right)

        if right_is_out_of_items:
            return 1

        left_subitem = left[i_l]
        right_subitem = right[i_l]
        
        sub_items_in_order = compare_input_order(left_subitem, right_subitem)

        if sub_items_in_order != 0:
            return sub_items_in_order
        
    # if we run out of items, and the lists are the same length, can't make any conclusions
    if len(left) == len(right):
        return 0
    
    # if we iterate through all of left items, and the left list is shorter, it's in order
    return -1



import functools
import math



def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    divider_packets = ([[2]], [[6]])

    parsed_lines = list(eval(line.strip()) for line in lines if not line.strip() == "") 

    parsed_lines.extend(divider_packets)

    print ("\n".join(str(line) for line in parsed_lines))

    sorted_lines = sorted(parsed_lines, key = functools.cmp_to_key(compare_input_order))

    print ("\n".join(str(line) for line in sorted_lines))

    divider_indexes = tuple(sorted_lines.index(divider) for divider in divider_packets)

    print ("divider_indexes: {idxs}".format(idxs = ", ".join(str(i + 1) for i in divider_indexes)))

    decoder_key = math.prod(i + 1 for i in divider_indexes)

    print ("decoder key: {d}".format(d = str(decoder_key)))

  


    
if __name__ == "__main__":
    main()