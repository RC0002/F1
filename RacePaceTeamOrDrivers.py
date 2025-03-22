import fastf1
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
pd.options.mode.chained_assignment = None  # default='warn'
import Functions


#ff1.Cache.enable_cache('/Users/Federico/Library/Caches/fastf1')

#Stampa lo stint completo dei team
def executeStintDriverOrTeam(nameRace,yearRace,teams):
    # FastF1's default color scheme
    plotting.setup_mpl()
    plt.rcParams['figure.figsize'] = [25, 15]

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

    #--------------------------------------------------
    session = ff1.get_session(yearRace, nameRace, 'R')
    session.load()
    laps=session.laps
    i = 0
    fig , ax = plt.subplots(1)
    ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))
    fig.suptitle(f"{session.event.year} {session.event.EventName} - {session.name} - {teams}")

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    for i in range(len(session.results.index)):
        ID = session.results.iloc[i].get("Abbreviation")  # get code of the pilot
        team = session.results.iloc[i].get("TeamName")
        # Make sure that two teammates don't get the same line style
        linestyle = '-' if team not in visualized_teams else ':'
        if team in teams or ID in teams:
            lap_id = laps.pick_drivers(ID).pick_accurate()
            lapp = laps.pick_drivers(ID)
            colorq = ff1.plotting.team_color(team)
            plt.plot(lap_id['LapNumber'], lap_id['LapTime'],label=ID ,color=colorq,linewidth=1.5, linestyle=linestyle)
            j=0
            while j<len(lap_id['LapNumber']-1):
                lap=lap_id.iloc[j]
                if lap.Compound == 'SOFT':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='r',marker='o',markersize=6, linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq,markerfacecolor='r', marker='D',markersize=6, linestyle=linestyle)
                elif lap.Compound == 'MEDIUM':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='y',marker='o',markersize=6, linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq,markerfacecolor='y', marker='D',markersize=6, linestyle=linestyle)

                elif lap.Compound == 'HARD':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='w',marker='o',markersize=6, linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq,markerfacecolor='w', marker='D',markersize=6, linestyle=linestyle)
                elif lap.Compound == 'WET':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='b',marker='o',markersize=6, linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq,markerfacecolor='b', marker='D',markersize=6, linestyle=linestyle)
                elif lap.Compound == 'INTERMEDIATE':
                    if lap.FreshTyre:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='g',marker='o',markersize=6, linestyle=linestyle)
                    else:
                        ax.plot(lap['LapNumber'], lap['LapTime'],color=colorq, markerfacecolor='g', marker='D',markersize=6, linestyle=linestyle)
                j=j+1

                plt.ylabel('Laptime')
                plt.xlabel('Lap')
            SC = lapp.loc[lapp['TrackStatus'] == '4']
            #print(len(SC))
            VSC = lap_id.loc[lap_id['TrackStatus'] == '6']
            #print(VSC)
        visualized_teams.append(team)

    #print("AAAAAAAAAAAAA"+str(visualized_teams))
    ax.legend(loc="lower right")
    #fig.yticks(fontsize=5)
    #fig.xticks(fontsize=5)
    plt.grid(linewidth=0.09, color="grey")
    ax.xaxis.grid(False, 'minor')
    ax.yaxis.grid(False, 'minor')
    ax.spines[['right', 'top']].set_visible(False)


    Functions.savePlotInFile(plt,nameRace,yearRace,"\Race\\" +"R_Pace " + str(teams),"Race")
    print("Fine")


#Stampa i stint separati per gomma dei piloti
def executeStintOfSomeDrivers(nameRace,yearRace,drivers):
    typeOfSession = 'R'
    #fastf1.Cache.enable_cache('/Users/Federico/Library/Caches/fastf1')  # optional but recommended
    plotting.setup_mpl()
    plt.rcParams['figure.figsize'] = [25, 15]

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

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

    race = fastf1.get_session(yearRace, nameRace, typeOfSession)
    race.load()

    # comntrolla il numero di stint massimo e crea i relativi plot
    numStint = 0

    for d in drivers:
        laps = race.laps.pick_driver(d).pick_accurate()
        #print(laps.LapNumber.size)
        numStint = 0
        if(laps.LapNumber.values.size > 0):
            #print(d)
            #print(laps["LapNumber"].values)
            #print( laps.LapNumber.values.size)
            #print( laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]])
            tmp = laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]].iloc[0].Stint
            if tmp > numStint:
                numStint = tmp

    fig, ax = plt.subplots(int(numStint))
    fig.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} - {drivers}")

    posStampa=0
    # ------------------------------------
    for d in drivers:
        driver = race.laps.pick_driver(d).pick_accurate()
        #print(d)
        #---------------------------------------------------------
        #analisi stint di gara
        # Get laps of the driver
        #ottengo il colore della squadra per colorarlo
        team = race.get_driver(d)["TeamName"]
        color = ff1.plotting.team_color(team)

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
                linestyle = '-' if team not in visualized_teams else ':'

                if l.Compound.max() == 'SOFT':
                    if l.FreshTyre.max():
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='o',label=d, linestyle=linestyle)
                    else:
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='D', label=d, linestyle=linestyle)
                elif l.Compound.max() == 'MEDIUM':
                    if l.FreshTyre.max():
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='o', label=d, linestyle=linestyle)
                    else:
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='D', label=d, linestyle=linestyle)
                elif l.Compound.max() == 'HARD':
                    if l.FreshTyre.max():
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='o', label=d, linestyle=linestyle)
                    else:
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='D', label=d, linestyle=linestyle)
                elif l.Compound.max() == 'WET':
                    if l.FreshTyre.max():
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='o', label=d, linestyle=linestyle)
                    else:
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='D', label=d, linestyle=linestyle)
                elif l.Compound.max() == 'INTERMEDIATE':
                    if l.FreshTyre.max():
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='o', label=d, linestyle=linestyle)
                    else:
                        ax[i].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='D', label=d, linestyle=linestyle)

                ax[i].set(ylabel='Laptime', xlabel='Lap')
                ax[i].legend(loc="upper right")
                ax[i].grid(linewidth=0.09, color="grey")
                ax[i].xaxis.grid(False, 'minor')
                ax[i].yaxis.grid(False, 'minor')
                ax[i].spines[['right', 'top']].set_visible(False)

                # Hide x labels and tick labels for top plots and y ticks for right plots.
                for a in ax.flat:
                    a.label_outer()
        visualized_teams.append(team)

    if (typeOfSession == 'R'):
        NameSession = "Race"
    else:
        NameSession = "FreePractice"


    Functions.savePlotInFile(plt, nameRace, yearRace,"\\"+NameSession+"\\" +typeOfSession+"_PaceStint " + str(drivers), NameSession)
    #print(nameRace)
    print("Fine")
