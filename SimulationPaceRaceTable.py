# Genera Tabella per Numbers (Passi Gara pilota a scelta)
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd


laps = ff1.get_session(2022, 'Spain', 'FP2').load_laps()
allLAPS = laps.pick_drivers('PER')
print(allLAPS)

f = open("tempi.txt", "w")

print(type(allLAPS))
print(" LapTime,             LapNumber Stint  Sector1Time                Sector2Time                 Sector3Time             Compound FreshT   SpeedI1, SpeedI2   SpeedFL   SpeedST",file=f)
for i in allLAPS.pick_accurate().iterlaps():
    if i[1]['LapNumber'] < 10:
        if i[1]['Compound'] == "SOFT":
            with open("tempi.txt", "a") as f:
                print(i[1]['LapTime'], "    ", i[1]['LapNumber'], "   ", i[1]['Stint'], "   ", i[1]['Sector1Time'], "   ",i[1]['Sector2Time'], "   ", i[1]['Sector3Time'], "   ",
                  i[1]['Compound']," ", i[1]['FreshTyre'], "   ", i[1]['SpeedI1'], "   ", i[1]['SpeedI2'], "   ",i[1]['SpeedFL'], "   ", i[1]['SpeedST'], file=f)
        else:
            with open("tempi.txt", "a") as f:
                print(i[1]['LapTime'],"    ", i[1]['LapNumber'],"   ", i[1]['Stint'],"   ", i[1]['Sector1Time'],"   ", i[1]['Sector2Time'],"   ", i[1]['Sector3Time'],"   ",
                        i[1]['Compound'],i[1]['FreshTyre'],"   ",i[1]['SpeedI1'],"   ",i[1]['SpeedI2'],"   ",i[1]['SpeedFL'],"   ",i[1]['SpeedST'],file=f)
    else:
        if i[1]['Compound'] == "SOFT":
            with open("tempi.txt", "a") as f:
                print(i[1]['LapTime'], "   ", i[1]['LapNumber'], "   ", i[1]['Stint'], "   ", i[1]['Sector1Time'], "   ",
                      i[1]['Sector2Time'], "   ", i[1]['Sector3Time'], "   ",
                      i[1]['Compound']," ", i[1]['FreshTyre'], "   ", i[1]['SpeedI1'], "   ", i[1]['SpeedI2'], "   ",
                      i[1]['SpeedFL'], "   ", i[1]['SpeedST'], file=f)
        else:
            with open("tempi.txt", "a") as f:
                print(i[1]['LapTime'], "   ", i[1]['LapNumber'], "   ", i[1]['Stint'], "   ", i[1]['Sector1Time'], "   ",
                      i[1]['Sector2Time'], "   ", i[1]['Sector3Time'], "   ",
                      i[1]['Compound'], i[1]['FreshTyre'], "   ", i[1]['SpeedI1'], "   ", i[1]['SpeedI2'], "   ",
                      i[1]['SpeedFL'], "   ", i[1]['SpeedST'], file=f)

f.close()