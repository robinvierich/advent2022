

class Leaderboard:
    top_values = []

    num_tracked_values = 0

    def __init__(self, num_tracked_values, default_value = -1):
        self.num_tracked_values = num_tracked_values

        self.top_values = [default_value] * self.num_tracked_values

    # add a value to the leaderboard if it's > than the current values on the leaderboard
    def try_add_to_leaderboard(self, value):
        
        for i, top_value in enumerate(self.top_values):
            if value > top_value:
                self.top_values.insert(i, value)
                self.top_values.pop()
                return i
        
        return -1



class FoodInventory:


    def __init__(self, lines):
        current_elf_calorie_sum = 0
        i_elf = 0

        self.elf_calories = {}
        self.calorie_leaderboard = Leaderboard(3)


        for line in lines:

            if not line or line == "\n":
                self.elf_calories[i_elf] = current_elf_calorie_sum

                self.calorie_leaderboard.try_add_to_leaderboard(current_elf_calorie_sum)

                i_elf += 1
                current_elf_calorie_sum = 0

            else:

                calories = int(line)
                current_elf_calorie_sum += calories 


def main():

    lines = []

    import os

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    with open("input.txt", 'r') as f:
        lines = f.readlines()

    food_inventory = FoodInventory(lines)

    top_3_elf_calories = sum(food_inventory.calorie_leaderboard.top_values)

    print("top 3 max calories {calories}".format(calories = top_3_elf_calories))



    
if __name__ == "__main__":
    main()