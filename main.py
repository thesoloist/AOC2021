# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Day5 import *


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
    # day3_power = day3_1(day3_input, 12)
    # print(f"Day 3-1 power = {day3_power}")
    # day3_life = day3_2(day3_input, 12)
    # print(f"Day 3-2 life support rating = {day3_life}")
    # day4_score = day4_1()
    # print(f"Day 4-1 score = {day4_score}")
    # day4_score = day4_2()
    # print(f"Day 4-2 score = {day4_score}")
    day5_cross = day5(False)
    print(f"Day 5-1 cross = {day5_cross}")
    day5_cross = day5(True)
    print(f"Day 5-2 cross = {day5_cross}")