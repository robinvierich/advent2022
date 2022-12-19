import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines


def is_in_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left == right:
            return None
        else:
            return False

    if isinstance(left, list) and not isinstance(right, list):
        return is_in_order(left, [right])

    if not isinstance(left, list) and isinstance(right, list):
        return is_in_order([left], right)
    
    for i_l in range(len(left)):

        right_is_out_of_items = i_l >= len(right)

        if right_is_out_of_items:
            return False

        left_subitem = left[i_l]
        right_subitem = right[i_l]
        
        sub_items_in_order = is_in_order(left_subitem, right_subitem)

        if sub_items_in_order is not None:
            return sub_items_in_order
        
    # if we run out of items, and the lists are the same length, can't make any conclusions
    if len(left) == len(right):
        return None
    
    # if we iterate through all of left items, and the left list is shorter, it's in order
    return True






def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    strpairs = ((lines[i - 1], lines[i]) for i in range(1, len(lines), 3))

    pairs = ((eval(left.strip()), eval(right.strip())) for left, right in strpairs)
    
    sum = 0

    for i, (left, right) in enumerate(pairs):

        in_order = is_in_order(left, right)

        if in_order:
            sum += (i + 1)

        print(left)
        print(right)
        print("{i} in order? {in_order}".format(i = i, in_order = in_order))

    print("sum {} ".format(sum))

    
if __name__ == "__main__":
    main()