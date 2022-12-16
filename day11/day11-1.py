import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from thirdparty.parse.parse import *

import math



class Operand:
    def get_value(self, prev_value):
        return None

class LiteralOperand(Operand):
    def __init__(self, literal_value) -> None:
        self.literal_value = literal_value
    
    def get_value(self, prev_value):
        return self.literal_value
    
    def __str__(self) -> str:
        return str(self.literal_value)
        

class PrevValueOperand(Operand):
    def get_value(self, prev_value):
        return prev_value

    def __str__(self) -> str:
        return "old"

    


class Operation:
    def __init__(self, operands) -> None:
        self.operands = operands

    def execute(self, state):
        pass

class MultOperation(Operation):
    def execute(self, prev_value):
        values = (op.get_value(prev_value) for op in self.operands)
        return math.prod(values)

    def __str__(self) -> str:
        return " * ".join(str(op) for op in self.operands)

class AddOperation(Operation):
    def execute(self, prev_value):
        values = (op.get_value(prev_value) for op in self.operands)
        return sum(values)
    
    def __str__(self) -> str:
        return " + ".join(str(op) for op in self.operands)



def parse_operand(operandstr: str):
    if operandstr == "old":
        return PrevValueOperand()
    else:
        return LiteralOperand(int(operandstr))


def parse_operands(opstr: str, operationchar: str):

    opstr_after_equals = opstr[opstr.index("=") + 1:]

    args = (arg.strip() for arg in opstr_after_equals.split(operationchar))

    return tuple(parse_operand(op) for op in args)


def parse_operation(opstr: str):
    if "*" in opstr:
        return MultOperation(parse_operands(opstr, "*"))

    if "+" in opstr:
        return AddOperation(parse_operands(opstr, "+"))



class Item:
    def __init__(self, worry_level) -> None:
        self.worry_level = worry_level
    
    def __str__(self) -> str:
        return str(self.worry_level)



class DivisiblePredicate:
    def __init__(self, denom : int) -> None:
        self.denom = denom
    
    def check(self, value):
        return (value % self.denom) == 0
    

    def __str__(self) -> str:
        return "val % {denom}".format(denom = self.denom)



def parse_predicate(pred_str: str):
    pred_format = "divisible by {:d}"

    denom = parse(pred_format, pred_str.strip())[0]

    return DivisiblePredicate(denom)


class ThrowAction:
    def __init__(self, target_id) -> None:
        self.target_id = target_id
    
    #def execute(self, monkies, src_id, item) -> None:
        #monkies[src_id].items.remove(item)
        #monkies[self.target_id].items.append(item)
    
    def __str__(self) -> str:
        return "throw to {id}".format(id = self.target_id)


def parse_action(actionstr : str) -> ThrowAction:
    action_format = "throw to monkey {:d}"
    monkey_id = parse(action_format, actionstr.strip())[0]

    return ThrowAction(monkey_id)


class Monkey:
    def __init__(self, id: int, items: list[Item], operation : Operation, test :DivisiblePredicate, test_pass_action :ThrowAction, test_fail_action:ThrowAction) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.test_pass_action = test_pass_action
        self.test_fail_action = test_fail_action
    
    def __str__(self) -> str:
        return "Monke {id}, {items}".format(# - run {operation}, if {test}: {test_pass_action}, else: {test_fail_action}".format(
        #return "Monke {id}, {items} - run {operation}, if {test}: {test_pass_action}, else: {test_fail_action}".format(
            id = self.id,
            items = ", ".join(str(item) for item in self.items),
            operation = str(self.operation),
            test = str(self.test),
            test_pass_action = str(self.test_pass_action),
            test_fail_action = str(self.test_fail_action),
        )



def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    lines_per_monkey = 7

    num_monkies = len(lines) // lines_per_monkey

    monkies = []

    for i in range(num_monkies):
        i_line_base = i * lines_per_monkey
        monkey_id = parse("Monkey {:d}:\n", lines[i_line_base])[0]

        itemsstr = parse("  Starting items: {}\n", lines[i_line_base + 1])[0]
        items = list(Item(int(worry_level_str.strip())) for worry_level_str in itemsstr.split(","))

        opstr = parse("  Operation: {}\n", lines[i_line_base + 2])[0]
        operation = parse_operation(opstr)

        teststr = parse("  Test: {}\n", lines[i_line_base + 3])[0]
        test = parse_predicate(teststr)

        test_pass_actionstr = parse("    If true: {}\n", lines[i_line_base + 4])[0]
        test_pass_action = parse_action(test_pass_actionstr)

        test_fail_actionstr = parse("    If false: {}\n", lines[i_line_base + 5])[0]
        test_fail_action = parse_action(test_fail_actionstr)

        monkey = Monkey(monkey_id, items, operation, test, test_pass_action, test_fail_action)

        monkies.append(monkey)

    
    print("\n".join(str(monkey) for monkey in monkies))

    num_inspections = {}

    for round in range(20):
        for monkey in monkies:
            item_target_ids = {}

            old_values = tuple(item.worry_level for item in monkey.items)

            for item in monkey.items:
                # perform op (inspect)
                item.worry_level = monkey.operation.execute(item.worry_level)

                num_inspections[monkey] = num_inspections.setdefault(monkey, 0) + 1

                # divide worry by 3
                item.worry_level = item.worry_level // 3

                # check test
                # perform result action
                if monkey.test.check(item.worry_level):
                    item_target_ids[item] = monkey.test_pass_action.target_id
                else:
                    item_target_ids[item] = monkey.test_fail_action.target_id
            

            new_values = tuple(item.worry_level for item in monkey.items)
            
            for item, target_id in item_target_ids.items():
                monkey.items.remove(item)
                monkies[target_id].items.append(item)

            #print("    {}".format(", ".join(str(old) for old in old_values)))
            #print("    {}".format(", ".join(str(new) for new in new_values)))

            #print("{src} -> {tgts}".format(src = monkey.id, tgts = ", ".join(str(id) for id in item_target_ids.values())))


        
        print("== AFTER ROUND {round} ==".format(round = round + 1))

        print("\n".join(str(monkey) for monkey in monkies))
        print("")

    for monkey, num in num_inspections.items():
        print("Monkey {id} inspections: {num}".format(id = monkey.id, num = num))






    
if __name__ == "__main__":
    main()