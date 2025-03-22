import fastf1
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import make_interp_spline
pd.options.mode.chained_assignment = None  # default='warn'
import Functions


#ff1.Cache.enable_cache('/Users/Federico/Library/Caches/fastf1')

#---------------------------------------------------

#Stampa i stint separati dei piloti
def executeSimulationStintOfSomeDrivers(nameRace,yearRace,drivers,typeOfSession,secondiDaConsiderare):
    #fastf1.Cache.enable_cache('/Users/Federico/Library/Caches/fastf1')  # optional but recommended
    plotting.setup_mpl()

    #Style del testo------------------------
    large = 20;
    med = 9;
    small = 6
    params = {'axes.titlesize': large,
              'legend.fontsize': med,
              'figure.figsize': (16, 10),
              'axes.labelsize': med,
              'axes.titlesize': med,
              'xtick.labelsize': med,
              'ytick.labelsize': med,
              'figure.titlesize': large
              }
    plt.rcParams.update(params)
    plt.style.use('seaborn-v0_8-whitegrid')
    #---------------------------------------

    race = fastf1.get_session(yearRace, nameRace, typeOfSession)
    race.load()

    # comntrolla il numero di stint massimo e crea i relativi plot
    numStint = 0

    for d in drivers:
        laps = race.laps.pick_drivers(d).pick_accurate()
        numStint = 0
        if(laps.LapNumber.values.size > 0):
            #print(laps.LapNumber.size)
            #print(d)
            #print(laps["LapNumber"].values)
            #print( laps.LapNumber.values.size)
            #print( laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]])
            tmp = laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]].iloc[0].Stint
            if tmp > numStint:
                numStint = tmp

    fig, ax = plt.subplots(3)
    #ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))
    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    colors = []

    posStampa=0
    # ------------------------------------
    for d in drivers:
        driver = race.laps.pick_driver(d).pick_accurate()
        #---------------------------------------------------------
        #analisi stint di gara
        # Get laps of the driver
        #ottengo il colore della squadra per colorarlo
        team = race.get_driver(d)["TeamName"]
        color = ff1.plotting.get_team_color(team,race, colormap='official', exact_match=False)
        colors.append(color)
        laps = race.laps.pick_driver(d).pick_accurate()
        if (laps.LapNumber.values.size > 0):
            #print(laps.LapNumber.size)
            numStint = laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]].iloc[0].Stint
            for i in range(int(numStint)):
                #print(i)
                #We are only analyzing stint 1, so select that one
                l = laps.loc[laps['Stint'] == i+1]

                l['RaceLapNumber'] = l['LapNumber'] - 1

                full_distance_ver_ric = pd.DataFrame()
                summarized_distance_ver_ric = pd.DataFrame()
                tmp=laps.loc[laps['Stint'] == i+1]
                linestyle = '-' if team not in visualized_teams else ':'
                try:
                    tmp = tmp.drop(tmp.loc[tmp['LapTime'] >= (l.pick_fastest(d).get("LapTime") + secondiDaConsiderare)].index).LapNumber.values.size
                except:
                    tmp=0
                if(tmp>2):
                    fig.suptitle(" Stint comparison")
                    #print(l.pick_fastest(d).get("LapTime") + '00:00:8.000000')
                    l.drop(l.loc[l['LapTime'] >= (l.pick_fastest(d).get("LapTime") + secondiDaConsiderare)].index,inplace=True)
                    if l.Compound.max() == 'SOFT':
                        if l.FreshTyre.max():
                            ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='o',label=d, linestyle=linestyle)
                        else:
                            ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='D', label=d, linestyle=linestyle)

                    elif l.Compound.max() == 'MEDIUM':
                        if l.FreshTyre.max():
                            ax[1].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='o', label=d, linestyle=linestyle)
                        else:
                            ax[1].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='D', label=d, linestyle=linestyle)

                    elif l.Compound.max() == 'HARD':
                        if l.FreshTyre.max():
                            ax[2].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='o', label=d, linestyle=linestyle)
                        else:
                            ax[2].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='D', label=d, linestyle=linestyle)
                    '''
                    elif l.Compound.max() == 'WET':
                        if l.FreshTyre.max():
                            ax[3].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='o', label=d)
                        else:
                            ax[3].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='D', label=d)
                    elif l.Compound.max() == 'INTERMEDIATE':
                        if l.FreshTyre.max():
                            ax[4].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='o', label=d)
                        else:
                            ax[4].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='D', label=d)
                    '''
                    ax[0].set(ylabel='SOFT', xlabel='Lap')
                    ax[0].legend(loc="lower right")
                    ax[1].set(ylabel='MEDIUM', xlabel='Lap')
                    ax[1].legend(loc="lower right")
                    ax[2].set(ylabel='HARD', xlabel='Lap')
                    ax[2].legend(loc="lower right")

                    ax[0].grid(linewidth=0.09, color="grey")
                    ax[0].xaxis.grid(False,'minor')
                    ax[0].yaxis.grid(False, 'minor')
                    ax[0].spines[['right', 'top']].set_visible(False)
                    ax[1].grid(linewidth=0.09, color="grey")
                    ax[1].xaxis.grid(False,'minor')
                    ax[1].yaxis.grid(False, 'minor')
                    ax[1].spines[['right', 'top']].set_visible(False)
                    ax[2].grid(linewidth=0.09, color="grey")
                    ax[2].xaxis.grid(False,'minor')
                    ax[2].yaxis.grid(False, 'minor')
                    ax[2].spines[['right', 'top']].set_visible(False)
        visualized_teams.append(team)


    if (typeOfSession == 'R'):
        NameSession = "Race"
    elif typeOfSession == 'test':
        NameSession = "test"
    else:
        NameSession = "FreePractice"

    plt.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} - {drivers}")

    Functions.savePlotInFile(plt, nameRace, yearRace,"\\"+NameSession+"\\" +typeOfSession+"_PaceStint" + str(drivers), NameSession)
    return fig