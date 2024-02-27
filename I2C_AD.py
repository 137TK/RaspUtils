# -*- coding: utf-8 -*-
import smbus
from time import sleep
import time
import datetime
import sys
import os
import argparse
import csv

bus = smbus.SMBus(1)

# args setting

parser = argparse.ArgumentParser()

parser.add_argument("--mode", help="measurement mode (console/data save). default=console", default="console")
parser.add_argument("--time", help="measurement time [s]. default=5(data_save)/inf(console)", default="5")
parser.add_argument("--iter", help="iteration of program. default=inf", default="inf")
parser.add_argument("--data_num", help="sample number of mean. default=10", default="10")

args = parser.parse_args()

data_num = int(args.data_num)
time_max = float(args.time)
iter_max = float(args.iter)
measurement = args.mode


if( (measurement != "console") and (measurement !="data_save") ):
    print("measurement mode is not \"console\" or \"data_save\" ")
    exit()


start_time = time.time()


# constant
address = 0x4b
register = 0x00
meter_div = 4
meter_max = 6 #[V]
calib = 0.00505/8.113

# init 
i = 0
i_old = 0
mean = 0
meter_unit = ""
meter_line_str = ""
lasp = 0

for idx in range(meter_max):
    meter_unit += "{}".format(idx) + " "*(meter_div)

meter_unit = meter_unit + "{} [V]".format(meter_max)
meter_line_str = ("|" + "-"*meter_div)*meter_max + "|"
meter = ""

dt_time = datetime.datetime.now()

if( measurement != "console"):
    f = open("./result_{}:{}.csv".format(dt_time.hour, dt_time.minute), "a")
    writer = csv.writer(f)
    writer.writerow(["Voltage","Time", "Iterations"])
    print("measurement mode is data_save")
    print("please wait {} seconds....".format(time_max))
else:
    time_max = float("inf")

os.system("clear")
print(meter_unit)
print(meter_line_str)

try:
    while True:
        word = bus.read_word_data(address, register)
        data = (word & 0xff00 ) >> 8 | (word & 0x00ff ) << 8
        data = data >> 3

        mean = mean + data

        
        if(i % data_num == 1 ):
            lasp = time.time() - start_time
            mean = mean * calib / ((i - i_old))

            if(measurement == "console"):
                meter_volume = int(mean*(meter_max*(meter_div+1))/meter_max)
                meter = "#" + "#"*meter_volume + " "*(61 - meter_volume)
                print(meter + "\nTime : {:.2f} [s], Voltage = {:.3f} [V] \033[2A".format(lasp, mean), end="")
                print()
            else:
                writer.writerow([mean,lasp, i])
            
            i_old = i

        # sleep(1/data_num)
        i = i + 1

        if(i > iter_max):
            f.close()
            break

        if(lasp > time_max):
            f.close()
            break
except KeyboardInterrupt:
    f.close()
    pass
except NameError:
    pass

f.close()
