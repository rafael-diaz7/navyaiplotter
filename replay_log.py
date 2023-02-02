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

import matplotlib.pyplot as plt
from matplotlib import animation

from data_generator import existing_file_generator

# Define some empty lists to hold our data
# These are global scope, so all functions can access
ships_x, ships_y, friend_x, friend_y, enemy_x, enemy_y = [], [], [], [], [], []

# def yielder(ship_fp, friendly_fp, enemy_fp):
#     ship_line = existing_file_generator(ship_fp, 2)
#     friendly_line = existing_file_generator(friendly_fp, 3)
#     enemy_line = existing_file_generator(enemy_fp, 3)
#     yield (ship_line, friendly_line, enemy_line)

def plotter_init():
    """
    Initialize the plot axes and clear data in four lines in our plots
    """
    # analog_ax.set_ylim(-8, 1032)
    # analog_ax.set_yticks([0,256, 512, 768, 1024])
    # analog_ax.set_xlim(0, 10)
    # volt_ax.set_ylim(0, 5.0)
    # temp_ax.set_ylim(0, 100)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(-60000,60000)
    ax.set_ylim(-60000,60000)
    

    # Delete all elements from the list
    del ships_x[:]
    del ships_y[:]
    del friend_x[:]
    del friend_y[:]
    del enemy_x[:]
    del enemy_y[:]

    ship_plot.set_data([], [])
    friendly_plot.set_data([], [])
    enemy_plot.set_data([], [])

    return  ship_plot, friendly_plot, enemy_plot
    # Update the line with list data
    # ship_plot.set_data(time, a0_data)
    # friendly_plot.set_data(time, volt_data)
    # enemy_plot.set_data(time, a1_data)
    # t_line.set_data(time, temp_data)
    # fig.legend( bbox_to_anchor=(0.3, 0.3))

    # return a0_line, a1_line, v_line, t_line

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

    ship_separation = int(len(ships) / 2)
    friendly_separation = int(len(friendly_missiles) / 3)
    enemy_separation = int(len(enemy_missiles) / 3)
    ships_x, ships_y = ships[:ship_separation], ships[ship_separation:]
    friend_x, friend_y = friendly_missiles[:friendly_separation], friendly_missiles[friendly_separation:friendly_separation*2]
    enemy_x, enemy_y = enemy_missiles[:enemy_separation], enemy_missiles[enemy_separation:enemy_separation*2]

    ax.figure.canvas.draw()

    # Update the plots
    ship_plot.set_data(ships_x, ships_y)
    friendly_plot.set_data(friend_x, friend_y)
    enemy_plot.set_data(enemy_x, enemy_y)

    return ship_plot, friendly_plot, enemy_plot


# def save_data():
#     """
#     Save current plot image and stored data to files
#     """
#     # Note mixed use of single and double quotes to define f-string and date format
#     base_file_name = f'analog_data_{datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}'

#     # Save data if we are getting from Arduino serial
#     print(f"Saving plot image to {base_file_name} file ...")
#     fig.savefig(os.path.join("data", base_file_name+".png"))

#     print(f"Writing received data to {base_file_name} file ...")
#     with open(os.path.join("data", base_file_name+".csv"), "wt", newline="") as fin:
#         writer = csv.writer(fin,  delimiter=",")
#         writer.writerow(["# Time (ms)", "Pot", "Volts (V)", "Thermistor", "Temperature (F)"])
#         for i, t in enumerate(time_ms):  # pylint: disable=C0103
#             writer.writerow([t, a0_data[i], volt_data[i], a1_data[i], temp_data[i]])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program to plot receive and plot binary data from Arduino')  # pylint: disable=C0301
    parser.add_argument('--id', default=None, help="ID for log")
    parser.add_argument('--save', default=None, action='store_true', help="Saves animation as .mp4")
    # parser.add_argument('--port_name', default=None, help='Com port name\n   default: None - searches available ports for Arduino name')  # pylint: disable=C0301
    # parser.add_argument('--baud_rate', type=int, default=115200, help='Baud rate (default: 115200)')  # pylint: disable=C0301
    # parser.add_argument('--binary_format', default="<LHfHfB", help='Binary format to unpack (default: "<LHfHfB")')  # pylint: disable=C0301
    # parser.add_argument('--units', default=["ms", "", "V", "", "F"], help='Units for data formating as list of strings\n   default: ["ms", "", "V", "", "F"]')  # pylint: disable=C0301
    # parser.add_argument('--fake', action='store_true', default=False, help="Use a fake data generator to test plotting\n (fake data overrides serial)")  # pylint: disable=C0301
    # parser.add_argument('--file_name', default=None, help="Read existing file for data generation\n   (existing file overrides serial)")  # pylint: disable=C0301

    args = parser.parse_args()
    
    SHIP_FILEPATH = f"ship_locations_{args.id}.csv"
    FRIENDLY_TRACK_FILEPATH = f"friendly_missiles_locations_{args.id}.csv"
    ENEMY_TRACK_FILEPATH = f"enemy_missiles_locations_{args.id}.csv"

    print("Setting up the plot figures ...")
    fig, ax = plt.subplots()
    ship_plot, = ax.plot([], [], 'go', label="Ships")
    friendly_plot, = ax.plot([], [], 'bo', label="Friendly Missiles")
    enemy_plot, = ax.plot([], [], 'ro', label="Enemy Missiles")
    ax.legend()
    # fig, analog_ax = plt.subplots()
    # fig.subplots_adjust(right=0.75)
    # volt_ax = analog_ax.twinx()
    # temp_ax = analog_ax.twinx()
    # temp_ax.spines.right.set_position(("axes", 1.2))
    # analog_ax.set_xlim(0, 10.0)

    # v_line, = volt_ax.plot(time, volt_data, "b", lw=2, label="pot")
    # t_line, = temp_ax.plot(time, temp_data, "r", lw=2, label="temp")
    # a0_line, = analog_ax.plot(time, a0_data, "x", lw=2, label="a0")
    # a1_line, = analog_ax.plot(time, a1_data, "+", lw=2, label="a1")

    # tkw = dict(size=4, width=1.5)
    # analog_ax.tick_params(axis='y', colors='k', **tkw)
    # analog_ax.tick_params(axis='x', **tkw)
    # volt_ax.tick_params(axis='y', colors=v_line.get_color(), **tkw)
    # temp_ax.tick_params(axis='y', colors=t_line.get_color(), **tkw)

    # analog_ax.grid()

    # Set up generator function to retrieve data file
    data_generator_fn = None  # pylint: disable=C0103

    try:
        print(f"Attemping to use existing files with id {args.id} for plotting ...")
        data_generator_fn = existing_file_generator(SHIP_FILEPATH, FRIENDLY_TRACK_FILEPATH, ENEMY_TRACK_FILEPATH)
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
            writergif = animation.PillowWriter(fps=10)
            ani.save(f'replay{args.id}.gif', writer = writergif)

        print("Done!")
    else:
        print("Invalid data generator - cannot plot data!")

