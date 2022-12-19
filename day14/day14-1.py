import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines


def main():
    lines = read_input_lines(__file__, InputType.SAMPLE_INPUT)

    
if __name__ == "__main__":
    main()