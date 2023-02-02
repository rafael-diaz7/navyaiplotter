"""
Data generators used for analog_plotter

"""

import csv
import os
from itertools import islice
import numpy as np

def existing_file_generator(ship_fp, friend_fp, enemy_fp, delimiter=','):
    """
    Generator function that reads numeric data from an previously stored data file
    @param file_name
    @param dimensions of object being sent (2 for ship, 3 for missile)
    @param delimiter for csv file
    @yield list of lists of coordinates
    """
    ship_fp = file_checker(ship_fp)
    friend_fp = file_checker(friend_fp)
    enemy_fp = file_checker(enemy_fp)

    try:
        with open(ship_fp, "rt") as fin1:
            with open(friend_fp, "rt") as fin2:
                with open(enemy_fp, "rt") as fin3:
                    reader1 = csv.reader(fin1, delimiter=delimiter)
                    reader2 = csv.reader(fin2, delimiter=delimiter)
                    reader3 = csv.reader(fin3, delimiter=delimiter)
                    for line1, line2, line3 in zip(reader1, reader2, reader3):
                        yield (process_line(line1, 2), process_line(line2, 3), process_line(line3, 3))

    except Exception as exc:
        print(exc)
        raise exc

def file_checker(file_name):
    if ".csv" not in file_name:
        # Presume a base file name
        file_name += ".csv"

    if not os.path.exists(file_name):
        # Try to add data path relative to python folder
        file_name = os.path.join("data", file_name)

    if os.path.exists(file_name):
        print(f"Read data from existing file {file_name} ...")
    else:
        raise FileNotFoundError(f"No such file {file_name}")
    return file_name

def process_line(line, dimensions):
    num_objects = int(len(line) / dimensions)
    if not num_objects:
        return []
    x = []
    y = []
    z = []
    for i in range(num_objects):
        if dimensions == 3:
            x.append(float(line[3 * i]))
            y.append(float(line[3 * i + 1]))
            z.append(float(line[3 * i + 2]))
        elif dimensions == 2:
            x.append(float(line[2*i]))
            y.append(float(line[2*i+1]))
    return x + y + z


if __name__ == "__main__":
    print(process_line([1,2,3,4,5,6,7,8,9], 3))
    print(process_line([1,2,3,4,5,6], 2))
    # print(existing_file_generator("data/enemy_missiles_locations_0129.csv"))