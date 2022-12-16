from enum import Enum

class InputType(Enum):
    SAMPLE_INPUT = 1,
    REAL_INPUT = 2

def is_empty_line(line):
    return line.strip() == "" 

def read_input_lines(executing_file_path, input_type) -> list[str]:

    input_filename = ""

    if input_type == InputType.SAMPLE_INPUT:
        input_filename = "sample_input.txt"
    elif input_type == InputType.REAL_INPUT:
        input_filename = "input.txt"

    import os

    abspath = os.path.abspath(executing_file_path)
    dname = os.path.dirname(abspath)

    with open("{dir}/{filename}".format(dir = dname, filename = input_filename), 'r') as f:
        return f.readlines()


    
