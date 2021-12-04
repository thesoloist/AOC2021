# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Day1 import *
from Day2 import *
from Day3 import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    # day1_incr = Day1_1(day1_input)
    # print("Day 1-1 Increments = ", day1_incr)
    # day1_incr = Day1_2(day1_input)
    # print("Day 1-2 Increments = ", day1_incr)
    # (day2_horiz, day2_depth) = Day2_1(day2_input_str)
    # print(f"Day 2-1 horiz({day2_horiz}) * depth({day2_depth}) = {day2_depth * day2_horiz}")
    # (day2_horiz, day2_depth) = Day2_2(day2_input_str)
    # print(f"Day 2-2 horiz({day2_horiz}) * depth({day2_depth}) = {day2_depth * day2_horiz}")
    day3_power = day3_1(day3_input, 12)
    print(f"Day 3-1 power = {day3_power}")
    day3_life = day3_2(day3_input, 12)
    print(f"Day 3-2 life support rating = {day3_life}")
