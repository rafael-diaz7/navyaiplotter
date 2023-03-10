"""
Code to plot signals from Arduino for Mechatronics Lab 04

Based on code:
https://matplotlib.org/2.0.2/examples/animation/animate_decay.html
https://matplotlib.org/stable/gallery/animation/animate_decay.html
https://matplotlib.org/stable/gallery/spines/multiple_yaxis_with_spines.html
"""

import argparse
import csv
import datetime
import os
import sys
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.colors as mcolors
import matplotlib.cm as cm

from data_generator import existing_file_generator, pickle_file_generator

# Define some empty lists to hold our data
# These are global scope, so all functions can access
ships_x, ships_y, ships_health, friend_x, friend_y, enemy_x, enemy_y = [], [], [], [], [], [], []


def plotter_init():
    """
    Initialize the plot axes and clear data in four lines in our plots
    """
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(-60000,60000)
    ax.set_ylim(-60000,60000)
    

    # Delete all elements from the list
    del ships_x[:]
    del ships_y[:]
    del ships_health[:]
    del friend_x[:]
    del friend_y[:]
    del enemy_x[:]
    del enemy_y[:]

    ship_plot.set_offsets(np.column_stack(([],[])))
    friendly_plot.set_data([], [])
    enemy_plot.set_data([], [])

    return  ship_plot, friendly_plot, enemy_plot

def update_plotter(data):
    """
    Update the plotter with data from generator function
    """
    # update the data
    if data is None:
        print("No data to process!")
        return None

    ax.collections.clear()

    ships, friendly_missiles, enemy_missiles = data[0], data[1], data[2]  # pylint: disable=C0103

    ships_x, ships_y, ships_health = process_generator(ships, 3)
    ships_health = np.array(ships_health)
    color_map = {4: 'green', 3: 'yellow', 2: 'orange', 1: 'red'}
    colors = list(map(lambda h: color_map[h], ships_health))
    friend_x, friend_y, _ = process_generator(friendly_missiles, 3)
    enemy_x, enemy_y, _ = process_generator(enemy_missiles, 3)
    ax.figure.canvas.draw()

    # Update the plots
    ship_plot = ax.scatter(ships_x, ships_y, c=colors, cmap=cm.viridis, label="Ships")
    friendly_plot.set_data(friend_x, friend_y)
    enemy_plot.set_data(enemy_x, enemy_y)

    return ship_plot, friendly_plot, enemy_plot

def process_generator(yieled_list, num_features):
    return_list = []
    num_objects = int(len(yieled_list)/num_features)
    if not num_objects:
        return [[],[],[]]
    for i in range(num_features):
        return_list.append(yieled_list[i * num_objects : (i + 1) * num_objects])
    return return_list


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program to replay runs from the Navy AI Challenge')  # pylint: disable=C0301
    parser.add_argument('--id', default=None, help="ID for log")
    parser.add_argument('--save', default=None, action='store_true', help="Saves animation as .mp4")

    args = parser.parse_args()
    
    PICLKE_FILEPATH = os.path.join("data", f"run1_{args.id}")

    print("Setting up the plot figures ...")
    fig, ax = plt.subplots()
    ax.set_title(f"Replay ID: {args.id}")
    ship_plot = ax.scatter([], [], c=[], cmap=cm.viridis, label="Ships")
    friendly_plot, = ax.plot([], [], 'b^', label="Friendly Missiles")
    enemy_plot, = ax.plot([], [], 'rv', label="Enemy Missiles")
    ax.legend()

    # Set up generator function to retrieve data file
    data_generator_fn = None  # pylint: disable=C0103

    try:
        print(f"Attemping to use existing files with id {args.id} for plotting ...")
        data_generator_fn = pickle_file_generator(PICLKE_FILEPATH)
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(-1)
    if data_generator_fn:
        print("Begin plotting data ...")
        ani = animation.FuncAnimation(fig, update_plotter, data_generator_fn,
                                      blit=False, interval=10,
                                      repeat=False, init_func=plotter_init)

        # Start interactive plot - X to quit and continue to save
        plt.show()

        if args.save:
            ani.save(f"replay{args.id}.mpy4")

        print("Done!")
    else:
        print("Invalid data generator - cannot plot data!")

