import os

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt

import Functions

fastf1.Cache.enable_cache('\\Users\comer\Documents\F1 Data\cache')

def execute(nameRace,yearRace):

    # FastF1's default color scheme
    plotting.setup_mpl()
    plt.rcParams['figure.figsize'] = [16,10]
    session = ff1.get_session(yearRace, nameRace, 'R')
    race = fastf1.get_session(yearRace, nameRace, 'R')
    race.load()
    session.load()
    laps=session.laps
    i = 0

    #Style del testo------------------------
    large = 20;
    med = 9;
    small = 6
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              #'figure.figsize': (16, 10),
              'axes.labelsize': med,
              'axes.titlesize': med,
              'xtick.labelsize': med,
              'ytick.labelsize': med,
              'figure.titlesize': large
              }
    plt.rcParams.update(params)
    plt.style.use('seaborn-v0_8-whitegrid')
    #---------------------------------------

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    fig, ax = plt.subplots(1)
    ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))

    while i < 19:
        ID = session.results.iloc[i].get("Abbreviation")
        team = session.results.iloc[i].get("TeamName")
        if team == ('Red Bull Racing') or (team == 'Mercedes') or (team == 'Ferrari') or (team == 'McLaren') or (team == 'Alpine') or (team == 'AlphaTauri') or (team == 'Alfa Romeo') or (team == 'Williams') or (team == 'Haas F1 Team') or (team == 'Aston Martin'):
            lap_id = laps.pick_drivers(ID).pick_accurate()
            lapp = laps.pick_driver(ID)
            colorq = ff1.plotting.team_color(team)
            #print(team)
            #print(colorq)
            if(colorq=='#ffffff'):
                colorq = '#ccdbe4'
            linestyle = '-' if team not in visualized_teams else ':'
            ax.plot(lap_id['LapNumber'], lap_id['LapTime'],label=ID ,color=colorq, markerfacecolor='r',marker='o',linestyle=linestyle)
            j=0
            while j<len(lap_id['LapNumber']-1):
                lap=lap_id.iloc[j]
                if lap.Compound == 'SOFT':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'], color=colorq, markerfacecolor='r',marker='o',linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='r', marker='D',linestyle=linestyle)
                elif lap.Compound == 'MEDIUM':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='y',marker='o',linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='y', marker='D',linestyle=linestyle)

                elif lap.Compound == 'HARD':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='w',marker='o',linestyle=linestyle)
                    else:
                        plt.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='w', marker='D',linestyle=linestyle)
                elif lap.Compound == 'WET':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'], color=colorq, markerfacecolor='b',marker='o',linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='b', marker='D',linestyle=linestyle)

                elif lap.Compound == 'INTERMEDIATE':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'], color=colorq, markerfacecolor='g',marker='o',linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='g', marker='D',linestyle=linestyle)
                j=j+1

                plt.ylabel('Laptime')
                plt.xlabel('Lap')
            SC = lapp.loc[lapp['TrackStatus'] == '4']
            #print(len(SC))
            VSC = lap_id.loc[lap_id['TrackStatus'] == '6']
            #print(VSC)
        i = i + 1
        visualized_teams.append(team)
        #print(visualized_teams)

    ax.grid(linewidth=0.09, color="grey")
    ax.xaxis.grid(False, 'minor')
    ax.yaxis.grid(False, 'minor')
    ax.legend(loc="upper right")
    #ax.xaxis.grid(False, 'major')
    #ax.yaxis.grid(False, 'major')
    ax.spines[['right', 'top']].set_visible(False)

    fig.suptitle(f"{race.event.year} {race.event.EventName} - {race.name}")
    Functions.savePlotInFile(plt, nameRace, yearRace, "\Race\\" + "R_All", "Race")

def executeCompareOfDriverSameTeam(nameRace,yearRace):
    plotting.setup_mpl()
    plt.style.use('dark_background')
    plt.rcParams['figure.figsize'] = [30, 25]
    session = ff1.get_session(yearRace, nameRace, 'R')
    race = fastf1.get_session(yearRace, nameRace, 'R')
    race.load()
    session.load()
    laps = session.laps

    teams=Functions.getTeams(session.results)

    for t in teams:
        driverOfTeam = Functions.get_driversFromTeam(t,session.results)
        #print(driverOfTeam[0],driverOfTeam[1])
        Functions.plotDriverCompare(race,plt,session,ff1,driverOfTeam[0],driverOfTeam[1])

        dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici", str(yearRace) + "_" + nameRace)
        if not os.path.exists(dir):
            os.mkdir(dir)
        dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici\\" + str(yearRace) + "_" + nameRace + "\Race","CompareDrivers")
        if not os.path.exists(dir):
            os.mkdir(dir)
        plt.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} - {t}")
        Functions.savePlotInFile(plt, nameRace, yearRace,"\Race\CompareDrivers\\" + "R_All_"+str(t)+"", "Race")