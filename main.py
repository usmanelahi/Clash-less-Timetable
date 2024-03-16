import pandas as pd
import os
import random
import copy
import numpy as np
import math

desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

COURSES_NAME = ["Software Engineering", "Digital Image Processing", "Parallel & Dist Computing",
                "Organizational Behaviour", "Artificial Intelligence"]
CLASSROOMS = ["Seminar Hall", "CS-2", "CS-3", "CS-4", "CS-5", "CS-6", "CS-7", "CS-9", "CS-10", "CS-11",
              "CS-15", "CS-16", "E&M-1", "E&M-2", "E&M-3", "E&M-4", "E&M-5", "E&M-11", "CE-1", "CE-2",
              "CE-3", "CS-1", "CS-8", "E&M-16", "English Lab-1", "English Lab-2", "English Lab-3",
              "English Lab-4", "Lab(CS-1)", "Lab(CS-2A)", "Lab(CS-2B)", "Lab(CS-4)", "Lab(CS-6)",
              "Lab(CS-8)", "Lab(CS-9)", "Physics Lab", "Micro Lab", "Physics Lab", "Micro Lab",
              "Embedded Lab"]
TIME = ['8:30-10:00', '10:00-11:30', '11:30-1:00', '1:00-2:30', '2:30-4:00', '4:00-5:30', '5:30-7:00']
dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

FITNESS_CONDITIONS = []
COURSES = []
POPULATION = []
BUFFER = []
DAYS = [0, 0, 0, 0, 0, 0]
START = [0, 0, 0, 0, 0, 0]
POPULATION_SIZE = 500
BEST_FIT = 0.2
CROSSOVER = 0.4
MUTATION = 0.4

for i in range(5):
    COURSES.append([])

df = pd.read_csv('Schedule.csv')


def clear_console(): return os.system('cls')


def read_excel():
    index = 0
    row = 0
    while row < len(df):
        while row < len(df) and (str(df.iloc[row][0])).find(dayNames[index]) == -1:
            row += 1
        START[index] = row
        while row < len(df) and (str(df.iloc[row][0])).find(dayNames[index + 1]) == -1:
            DAYS[index] += 1
            row += 1
        index += 1
        if dayNames[index - 1] == 'Saturday':
            break


def take_user_input():
    print(COURSES_NAME)
    print('Choose the off day')
    print('#0 for Monday')
    print('#1 for Tuesday')
    print('#2 for Wednesday')
    print('#3 for Thursday')
    print('#4 for Friday')
    day = int(input('Option # '))
    off_days = [day]
    FITNESS_CONDITIONS.append(off_days)

    print('Choose # of consecutive classes')
    print('#1 for 1')
    print('#2 for 2')
    print('#3 for 3')
    consecutive = int(input('Option # '))
    FITNESS_CONDITIONS.append(consecutive)

    print('Choose last class time for the day')
    print('#0 for 4:00-5:30')
    print('#1 for 2:30-4:00')
    last = 6 - int(input('Option # '))
    FITNESS_CONDITIONS.append(last)

    print('Choose first class time for the day')
    print('#0 for 8:30-10:00')
    print('#1 for 10:00-11:30')
    print('#2 for 11:30-1:00')
    first = int(input('Option # '))
    FITNESS_CONDITIONS.append(first)


def isnan(value):
    try:
        return math.isnan(float(value))
    except:
        return False


def filter_courses():
    for _i in range(len(DAYS)):
        iteration = START[_i]
        while iteration < START[_i] + DAYS[_i] - 1:
            course = 0
            check = 0
            for j in (df.iloc[iteration]):
                if not isnan(j):
                    if j not in CLASSROOMS and j.find(dayNames[_i]) == -1:
                        for k in range(len(COURSES_NAME)):
                            if j.find(COURSES_NAME[k]) != -1:
                                if len(j) - len(COURSES_NAME[k]) <= 10:
                                    COURSES[k].append(j + " " + str(_i) + " " + str(course))
                check += 1
                if check % 9 == 0:
                    course += 1
            iteration += 1


def combine():
    for _i in range(len(COURSES)):
        avail = len(COURSES[_i])
        j = 0
        while j < avail:
            k = j + 1
            while k < avail:
                _split = COURSES[_i][k].split()
                if _split[-3] == COURSES[_i][j].split()[-3]:
                    COURSES[_i][j] += " " + _split[-2] + " " + _split[-1]
                    del COURSES[_i][k]
                    avail -= 1
                k += 1
            j += 1


class Sample:
    def __init__(self, timetable, fitness_val):
        self.timetable = timetable,
        self.fitness_val = fitness_val

    def remove_course_return_index(self, course_name):
        _days = []
        _time = []
        _section = ""
        days_count = 0
        for _itr in self.timetable:
            for day in _itr:
                time_count = 0
                for time in day:
                    index = 0
                    for course in time:
                        if course.find(course_name) != -1:
                            _section = course.split()[-1]
                            _days.append(days_count)
                            _time.append(time_count)
                            del time[index]
                        index += 1
                    time_count += 1
                days_count += 1
        return _days, _time, _section

    def __lt__(self, other):
        return self.fitness_val < other.fitness_val

    def __gt__(self, other):
        return self.fitness_val > other.fitness_val


def calculate_fitness(tt):
    value = 0
    for _i in FITNESS_CONDITIONS[0]:
        for j in tt[_i]:
            if len(j) != 0:
                value += 500
    for _i in tt:
        consecutive = 0
        for j in _i:
            if len(j) != 0:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive > FITNESS_CONDITIONS[1]:
                value += 2
            if len(j) > 1:
                value += (500 * len(j))
    for _i in tt:
        for j in range(FITNESS_CONDITIONS[2], 6):
            if len(_i[j]) != 0:
                value += 10
    for _i in tt:
        for j in range(0, FITNESS_CONDITIONS[3]):
            if len(_i[j]) != 0:
                value += 10
    return value


def generate_timetable():
    tt = []
    for _i in range(6):
        tt.append([])
        for j in range(7):
            tt[_i].append([])

    for _i in range(5):
        _split = COURSES[_i][random.randint(0, len(COURSES[_i]) - 1)].split()
        j = 0
        course = ""
        for j in range(len(_split)-5):
            course += _split[j] + " "
        course += _split[-5]
        tt[int(_split[-4])][int(_split[-3])].append(course)
        tt[int(_split[-2])][int(_split[-1])].append(course)
    return tt


def generate_population():
    for _i in range(POPULATION_SIZE):
        tt = generate_timetable()
        value = calculate_fitness(tt)
        sample_tt = Sample(tt, value)
        POPULATION.append(sample_tt)


def filter_best_fit():
    BUFFER.clear()
    for _i in range(int(BEST_FIT * POPULATION_SIZE)):
        BUFFER.append(POPULATION[_i])


def apply_crossover():
    for _i in range(int(CROSSOVER * POPULATION_SIZE)):
        # pick two parent samples at random
        parent_one = random.randint(0, POPULATION_SIZE // 2)
        parent_two = random.randint(parent_one + 1, POPULATION_SIZE - 1)
        # pick course to swap
        course = COURSES_NAME[random.randint(0, (len(COURSES_NAME) - 1))]
        child_1 = copy.deepcopy(POPULATION[parent_one])
        child_2 = copy.deepcopy(POPULATION[parent_two])

        child_1.remove_course_return_index(course)
        day_2, time_2, section_2 = child_2.remove_course_return_index(course)
        course_2 = course + " " + section_2
        child_1.timetable[0][day_2[0]][time_2[0]].append(course_2)
        child_1.timetable[0][day_2[1]][time_2[1]].append(course_2)
        BUFFER.append(child_1)


def apply_mutation():
    for _i in range(int(MUTATION * POPULATION_SIZE)):
        course = COURSES_NAME[random.randint(0, (len(COURSES_NAME) - 1))]
        # pick the sample on which you need to apply mutation on
        _parent = random.randint(0, POPULATION_SIZE - 1)
        mutant = copy.deepcopy(POPULATION[_parent])
        mutant.remove_course_return_index(course)
        _index = 0
        for _itr in COURSES:
            if _itr[0].find(course) != -1:
                break
            _index += 1
        index = random.randint(0, (len(COURSES[_index]) - 1))
        _split = COURSES[_index][index].split()
        j = 0
        course = ""
        for j in range(len(_split)-5):
            course += _split[j] + " "
        course += _split[-5]
        mutant.timetable[0][int(_split[-4])][int(_split[-3])].append(course)
        mutant.timetable[0][int(_split[-2])][int(_split[-1])].append(course)
        BUFFER.append(mutant)


def buffer_to_population():
    # helper function to copy data from buffer to population
    POPULATION.clear()
    for _i in range(POPULATION_SIZE):
        BUFFER[_i].fitness_val = calculate_fitness(BUFFER[_i].timetable[0])
        POPULATION.append(BUFFER[_i])
    BUFFER.clear()


read_excel()
del dayNames[-1]
filter_courses()
combine()

take_user_input()
generate_population()
POPULATION.sort()

itr = 0
clear_console()
print('CALCULATING...')

while POPULATION[0].fitness_val != 0 and itr < 100:
    # print(POPULATION[0].fitness_val, " Iteration : ", itr)
    filter_best_fit()
    apply_crossover()
    apply_mutation()
    buffer_to_population()
    POPULATION.sort()
    itr += 1

clear_console()

if POPULATION[0].fitness_val == 0:
    print("Target Reached")
else:
    print("Iteration Limit Reached (Best Samples)")

df_0 = pd.DataFrame(POPULATION[0].timetable[0], columns=TIME, index=dayNames)
print(df_0)
print('------------------------------------------------------------------------------------------------'
      '------------------------------------------------------------------------------------------------')
df_1 = pd.DataFrame(POPULATION[1].timetable[0], columns=TIME, index=dayNames)
print(df_1)
print('------------------------------------------------------------------------------------------------'
      '------------------------------------------------------------------------------------------------')

df_2 = pd.DataFrame(POPULATION[2].timetable[0], columns=TIME, index=dayNames)
print(df_2)
e = "e"
while e != "":
    e = input('Press enter key to exit')
