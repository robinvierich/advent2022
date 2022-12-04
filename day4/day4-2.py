import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines


class SectionWindow:

    def __init__(self, window_str):
        minstr, maxstr = window_str.split('-')

        self.min = int(minstr)
        self.max = int(maxstr)


    def is_fully_contained_within(self, other_window):
        return other_window.min <= self.min and other_window.max >= self.max

    def is_partially_contained_within(self, other_window):
        return (
            (other_window.min <= self.min and other_window.max >= self.min) 
            or (other_window.max >= self.max and other_window.min <= self.max)
        )




def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    num_fully_contained_pairs = 0
    num_partially_contained_pairs = 0

    for line in lines:
        window0str, window1str = line.split(",")

        window0, window1 = SectionWindow(window0str), SectionWindow(window1str)

        if window0.is_fully_contained_within(window1) or window1.is_fully_contained_within(window0):
            num_fully_contained_pairs += 1
        
        if window0.is_partially_contained_within(window1) or window1.is_partially_contained_within(window0):
            num_partially_contained_pairs += 1
        
    print("Num fully contained pairs {num}".format(num = num_fully_contained_pairs))
    print("Num partially contained pairs {num}".format(num = num_partially_contained_pairs))


    
if __name__ == "__main__":
    main()