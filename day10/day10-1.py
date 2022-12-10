import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from enum import Enum

class RegisterState:
    def __init__(self, X = 1) -> None:
        self.X = X


class ExecuteStatus(Enum):
    Running = 1
    Done = 2


# no-op instruction. base class
class Instruction:
    def start(self, state):
        yield ExecuteStatus.Done, state


class AddInstruction(Instruction):

    def __init__(self, num_to_add) -> None:
        self.num_to_add = num_to_add

    def start(self, state):
        yield ExecuteStatus.Running, state
        yield ExecuteStatus.Done, RegisterState(state.X + self.num_to_add)


def parse_instruction(line: str) -> Instruction:

    line = line.strip()

    if line.startswith("addx"):
        return AddInstruction(int(line.split(" ")[1]))
    elif line.startswith("noop"):
        return Instruction()
    else:
        print("oh no")
        return None

        




def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    cycle = 0

    instrs = [parse_instruction(line) for line in lines]

    state = RegisterState()
    curr_instr = None
    instr_gen = None

    signal_strengths = []

    while cycle <= 220 and len(instrs) > 0:
        cycle += 1

        # fetch next instruction
        if not curr_instr:
            curr_instr = instrs.pop(0)
            instr_gen = curr_instr.start(state)

        if (cycle % 40) == 20:
            signal_strength = cycle * state.X
            signal_strengths.append(signal_strength)
            print("X = {X} during cycle {cycle}. Strength = {strength}".format(X = state.X, cycle = cycle, strength = signal_strength ))

        # step instruction execution
        status, state = next(instr_gen)

        if status == ExecuteStatus.Done:
            curr_instr = None

    final_signal_str = sum(signal_strengths)
    print("sum of all signal strengths: {final_sum}".format(final_sum = final_signal_str))
            

    
if __name__ == "__main__":
    main()