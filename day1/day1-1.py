

class FoodInventory:

    def __init__(self, lines):
        self.elf_calories = {}
        self.max_calories = 1
        self.i_elf_max_calories = -1

        current_elf_calorie_sum = 0
        i_elf = 0

        for line in lines:


            if not line or line == "\n":
                self.elf_calories[i_elf] = current_elf_calorie_sum

                if current_elf_calorie_sum > self.max_calories:
                    self.max_calories = current_elf_calorie_sum
                    self.i_elf_max_calories = i_elf

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

    print("elf {i_elf} has max calories {calories}".format(i_elf = food_inventory.i_elf_max_calories, calories = food_inventory.max_calories))



    
if __name__ == "__main__":
    main()