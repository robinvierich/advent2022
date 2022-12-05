import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines, is_empty_line

from thirdparty.parse import parse


class CraneInstruction:

    def __init__(self, instruction_str) -> None:
        self.num_to_move, self.from_stack, self.to_stack = parse("move {:d} from {:d} to {:d}", instruction_str)


class CargoState:

    def __init__(self, cargo_strs) -> None:

        stack_strs = cargo_strs[:-1]
        stack_id_strs = cargo_strs[-1]


        # find columns in input strings where there may be a crate

        # index in columns array is the index of the stack this column relates to
        columns = []

        self.stack_ids = []
        self.stacks = []

        for col, stack_id_str in enumerate(stack_id_strs):
            if stack_id_str != " ":
                self.stack_ids.append(stack_id_str)
                self.stacks.append([])

                columns.append(col)
            

        for stack_str in reversed(stack_strs):
            length = len(stack_str)

            for i_stack, col in enumerate(columns):
                if col >= length:
                    break

                crate_at_col = stack_str[col]

                if crate_at_col != " ":
                    # we are looping in reverse here, so we can just push to the stack
                    self.stacks[i_stack].append(crate_at_col)
    
    def __str__(self) -> str:

        stack_strs = ["{i}  {stacks}".format(i = self.stack_ids[i], stacks = " ".join(stack)) for i, stack in enumerate(self.stacks)]

        return "\n".join(stack_strs)



def main():
    lines = read_input_lines(__file__, InputType.SAMPLE_INPUT)

    cargo_strs = []
    instr_strs = []

    hit_empty_line = False

    for line in lines:

        if is_empty_line(line):
            hit_empty_line = True
            continue

        if not hit_empty_line:
            cargo_strs.append(line.strip('\n'))
        else:
            instr_strs.append(line.strip('\n'))
    
    cargo_state = CargoState(cargo_strs)
    #crane_instructions = tuple(CraneInstruction(instr_str) for instr_str in instr_strs)


    print("cargo state: \n{cargo_state}".format(cargo_state = str(cargo_state)))

    


        





    
if __name__ == "__main__":
    main()