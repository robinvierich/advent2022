import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines, is_empty_line

from thirdparty.parse.parse import *


class CraneInstruction:
    instr_format = "move {:d} from {:d} to {:d}" 

    def __init__(self, instruction_str) -> None:
        self.num_to_move, self.from_stack_id, self.to_stack_id = parse(CraneInstruction.instr_format, instruction_str)

    def __str__(self) -> str:
        return CraneInstruction.instr_format.format(self.num_to_move, self.from_stack_id, self.to_stack_id)


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
                self.stack_ids.append(int(stack_id_str))
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
    
    def get_stack_from_id(self, stack_id):

        i_stack = self.stack_ids.index(stack_id)

        return self.stacks[i_stack]
        
    
    def __str__(self) -> str:

        stack_strs = ["{i}  {stacks}".format(i = self.stack_ids[i], stacks = " ".join(stack)) for i, stack in enumerate(self.stacks)]

        return "\n".join(stack_strs)


def apply_instruction(cargo_state, instr):

    from_stack = cargo_state.get_stack_from_id(instr.from_stack_id)
    to_stack = cargo_state.get_stack_from_id(instr.to_stack_id)

    for i in range(instr.num_to_move):
        if len(from_stack) > 0:
            to_stack.append(from_stack.pop())
    
    return cargo_state



def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

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
    crane_instructions = tuple(CraneInstruction(instr_str) for instr_str in instr_strs)


    print("cargo state: \n{cargo_state}".format(cargo_state = str(cargo_state)))
    print("instructions: \n{instructions}".format(instructions = "\n".join(str(crane_instr) for crane_instr in crane_instructions)))

    for instr in crane_instructions:
        cargo_state = apply_instruction(cargo_state, instr)


    print("cargo state: \n{cargo_state}".format(cargo_state = str(cargo_state)))





    
if __name__ == "__main__":
    main()