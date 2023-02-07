"""
Data generators used for analog_plotter

"""

import csv
import os
from itertools import islice
import numpy as np
import pickle

def pickle_file_generator(file_path):
    """
    Generator function that reads log file for a simulation run
    @param file_name leading to path
    @yield list of list coordinates [[x, y], [x, y]]
    """
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)

    for step in data:
        ship_locations = []
        enemy_missiles = []
        friendly_missiles = []
        step_info = data.get(step)
        asset_info = step_info.get("Assets")[1:]
        track_info = step_info.get("Tracks")
        for item in asset_info:
            # ship x, ship y, ship health
            ship_locations.extend([item[3][0], item[3][1], item[2]])

        for item in track_info:
            # missile x, missile y, missile z
            if "ENEMY" in item[1]:
                enemy_missiles.extend([item[3][0], item[3][1], item [3][2]])
            else:
                friendly_missiles.extend([item[3][0], item[3][1], item [3][2]])
        yield(process_line(ship_locations, 3), process_line(friendly_missiles, 3), process_line(enemy_missiles, 3))

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
    fp = "data/run1_0129"
    pickle_file_generator(fp)
    # print(process_line([1,2,3,4,5,6,7,8,9], 3))
    # print(process_line([1,2,3,4,5,6], 2))
    # print(existing_file_generator("data/enemy_missiles_locations_0129.csv"))