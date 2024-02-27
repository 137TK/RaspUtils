import numpy as np
import time
import datetime
import sys
import os
import argparse
import glob
import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()

parser.add_argument("--unit_name_y", help="the name of Y-axis. default=V", default="V")
parser.add_argument("--unit_name_x", help="the name of X-axis. default=sec", default="s")
parser.add_argument("--round_x", help="number of digits after the decimal point of X. default=2", default=2)
parser.add_argument("--round_y", help="number of digits after the decimal point of Y. default=2", default=2)


parser.add_argument("--path", help="path to csv. default ./*.csv", default="./*.csv")

args = parser.parse_args()
decimal_x = int(args.round_x)
decimal_y = int(args.round_y)

unit_name_y = args.unit_name_y
unit_name_x = args.unit_name_x


csv_file_paths = list(Path(".").glob(args.path))
csv_file_paths.sort(key=os.path.getmtime)
csv_file_paths = [file.name for file in csv_file_paths]
file_path = csv_file_paths[-1]

print("\n" + file_path + " is selected.")

image_name = file_path[0:0-3] + ".png"


data_array = []

with open(file_path, "rt") as file:
    reader = csv.reader(file)

    data = np.array([row for row in reader])
    data = data.T


x_label = data[1][0]
y_label = data[0][0]
x_data = data[1][1:]
y_data = data[0][1:]

x_data = [float(x) for x in x_data]
y_data = [float(y) for y in y_data]

fig = plt.figure()
ax = fig.add_subplot()

ax.plot(x_data, y_data, marker=".", linestyle="None")
ax.set_xlabel(x_label + " [{}]".format(unit_name_x))
ax.set_ylabel(y_label + " [{}]".format(unit_name_y))
ax.set_ylim(-1,6)
# plt.legend(loc="best")
ax.set_title(file_path)
plt.locator_params(axis="y", nbins=6)
plt.locator_params(axis="x", nbins=6)

plt.savefig(image_name)

print("save as {}".format(image_name))

