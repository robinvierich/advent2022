import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enum import Enum
from common.input_helper import InputType, read_input_lines


class Shape(Enum):
    UNKNOWN = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3



class RpsRoundResult(Enum):
    UNKNOWN = 0
    MY_WIN = 1
    MY_LOSS = 2
    DRAW = 3


op_str_to_shape = {"A" : Shape.ROCK, "B": Shape.PAPER, "C" : Shape.SCISSORS}

def parse_op_shape_str(shape_str):
    return op_str_to_shape.get(shape_str, Shape.UNKNOWN)


shape_to_reach_result = {
    RpsRoundResult.MY_WIN: {
        Shape.ROCK: Shape.PAPER, 
        Shape.PAPER: Shape.SCISSORS,
        Shape.SCISSORS: Shape.ROCK,
    },
    RpsRoundResult.DRAW: {
        Shape.ROCK: Shape.ROCK, 
        Shape.PAPER: Shape.PAPER,
        Shape.SCISSORS: Shape.SCISSORS,
    },
    RpsRoundResult.MY_LOSS: {
        Shape.ROCK: Shape.SCISSORS, 
        Shape.PAPER: Shape.ROCK,
        Shape.SCISSORS: Shape.PAPER,
    },
}


def get_shape_to_reach_desired_result(desired_result, op_shape):
    my_shape_from_op_shape = shape_to_reach_result[desired_result]
    my_shape = my_shape_from_op_shape[op_shape]

    return my_shape



my_str_to_result = {"X" : RpsRoundResult.MY_LOSS, "Y": RpsRoundResult.DRAW, "Z" : RpsRoundResult.MY_WIN}

def parse_my_shape_str(shape_str, op_shape):
    desired_result = my_str_to_result.get(shape_str, RpsRoundResult.UNKNOWN)

    return get_shape_to_reach_desired_result(desired_result, op_shape)



def did_shape1_win(shape1, shape2):
    if shape1 == Shape.ROCK and shape2 == Shape.SCISSORS:
        return True
    
    elif shape1 == Shape.SCISSORS and shape2 == Shape.PAPER:
        return True

    elif shape1 == Shape.PAPER and shape2 == Shape.ROCK:
        return True
    
    else:
        return False





def get_shape_score(shape):
    return shape.value


my_round_result_scores = {RpsRoundResult.MY_LOSS: 0, RpsRoundResult.DRAW: 3, RpsRoundResult.MY_WIN: 6}

def get_my_round_result_score(round_result):
    return my_round_result_scores.get(round_result, 0)


class RpsRound:
    my_shape = Shape.UNKNOWN
    op_shape = Shape.UNKNOWN

    def __init__(self, strategy_guide_line):

        op_shape_str, my_shape_str = strategy_guide_line.strip("\n").split(" ")

        self.op_shape = parse_op_shape_str(op_shape_str)
        self.my_shape = parse_my_shape_str(my_shape_str, self.op_shape)

    def calc_round_result(self):
        if self.my_shape == self.op_shape:
            return RpsRoundResult.DRAW
        else:
            if did_shape1_win(self.my_shape, self.op_shape):
                return RpsRoundResult.MY_WIN
            elif did_shape1_win(self.op_shape, self.my_shape):
                return RpsRoundResult.MY_LOSS
            else:
                return RpsRoundResult.UNKNOWN


    def calc_my_score(self):
        shape_score = get_shape_score(self.my_shape)

        round_result = self.calc_round_result()

        result_score = get_my_round_result_score(round_result)

        return shape_score + result_score




class RpsStrategyGuide:
    rounds = None

    def __init__(self, lines):

        self.rounds = tuple(RpsRound(line) for line in lines)
        
    def calc_my_score(self):
        return sum(round.calc_my_score() for round in self.rounds)




def main():
    lines = read_input_lines(__file__, InputType.SAMPLE_INPUT)

    strategy_guide = RpsStrategyGuide(lines)

    print("My score: {score}".format(score = strategy_guide.calc_my_score()))


    


if __name__ == "__main__":
    main()