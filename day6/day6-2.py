import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines


def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)


    for line in lines:

        line_len = len(line)

        for i in range(14, line_len):
            chars = line[i-14:i]

            all_different = len(set(chars)) == len(chars)

            if all_different:
                print("all different at index {i}".format(i = i))
                break


            



    
if __name__ == "__main__":
    main()