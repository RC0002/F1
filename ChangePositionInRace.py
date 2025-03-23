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
import streamlit as st
import Functions
import altair as alt


#ff1.Cache.enable_cache('/Users/Federico/Library/Caches/fastf1')

#---------------------------------------------------

#Stampa i stint separati dei piloti
def execute(nameRace,yearRace,drivers,typeOfSession,secondiDaConsiderare, isTest):
    fastf1.Cache.enable_cache('./Cache')  # optional but recommended
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

    if not isTest:
        race = fastf1.get_session(yearRace, nameRace, typeOfSession)
    else:
        race = fastf1.get_testing_session(yearRace, nameRace, typeOfSession)

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

    data_list = None
    colors = []
    driversForColor = []
    maxNLap = 0
    maxNumberPos = 0
    maxLapTime = 0

    posStampa=0
    # ------------------------------------
    for d in drivers:
        #---------------------------------------------------------
        #analisi stint di gara
        # Get laps of the driver
        #ottengo il colore della squadra per colorarlo
        team = race.get_driver(d)["TeamName"]
        color = ff1.plotting.get_team_color(team,race, colormap='official', exact_match=False)
        laps = race.laps.pick_driver(d)
        driversForColor.append(d)
        colors.append(color)
        if (laps.LapNumber.values.size > 0):
            #print(laps.LapNumber.size)
            numStint = laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]].iloc[0].Stint
            for i in range(0,int(numStint)):
                #print(i)
                #aggiungo i colori per il print del grafico


                #We are only analyzing stint 1, so select that one
                l = laps.loc[laps['Stint'] == i+1]

                l['RaceLapNumber'] = l['LapNumber'] - 1

                tmp=laps.loc[laps['Stint'] == i+1]
                linestyle = '-' if team not in visualized_teams else ':'
                #try:
                #    tmp = tmp.drop(tmp.loc[tmp['LapTime'] >= (l.pick_fastest(d).get("LapTime") + secondiDaConsiderare)].index).LapNumber.values.size
                #except:
                #    tmp=0
                #if(tmp>2):

                #if l.FreshTyre.max():
                    #ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='o',label=d, linestyle=linestyle)
                #else:
                    #ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='D', label=d, linestyle=linestyle)

                # ---------------------------------------------------------------
                l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                chart_dataSoft = pd.DataFrame({
                    "Driver": d,
                    "RaceLapNumber": l['RaceLapNumber'],
                    "Position": l['Position']
                })
                if(data_list is None):
                    data_list = chart_dataSoft
                else:
                    data_list = pd.concat([chart_dataSoft,data_list], ignore_index=True)


                # ---------------------------------------------------------------

                #ax[0].set(ylabel='SOFT', xlabel='Lap')
                #ax[0].legend(loc="lower right")
                #ax[1].set(ylabel='MEDIUM', xlabel='Lap')
                #ax[1].legend(loc="lower right")
                #ax[2].set(ylabel='HARD', xlabel='Lap')
                #ax[2].legend(loc="lower right")

                #ax[0].grid(linewidth=0.09, color="grey")
                #ax[0].xaxis.grid(False,'minor')
                #ax[0].yaxis.grid(False, 'minor')
                #ax[0].spines[['right', 'top']].set_visible(False)
                #ax[1].grid(linewidth=0.09, color="grey")
                #ax[1].xaxis.grid(False,'minor')
                #ax[1].yaxis.grid(False, 'minor')
                #ax[1].spines[['right', 'top']].set_visible(False)
                #ax[2].grid(linewidth=0.09, color="grey")
                #ax[2].xaxis.grid(False,'minor')
                #ax[2].yaxis.grid(False, 'minor')
                #ax[2].spines[['right', 'top']].set_visible(False)

                if (l['RaceLapNumber'].max() > maxNLap):
                    maxNLap = l['RaceLapNumber'].max()
                if (l['Position'].max() > maxNumberPos):
                    maxNumberPos = l['Position'].max()

        visualized_teams.append(team)



    # ---------------------------------------------------------------
    # Creazione di un grafico con Altair
    # Crea il grafico con Altair

    if data_list is not None:
        chartS = alt.Chart(data_list).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1)  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'Position:Q',
                scale=alt.Scale(domain=[maxNumberPos, 0])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'Position']  # Aggiungi tooltip interattivi
        ).properties(
            title='',  # Imposta il titolo del grafico
            width=600,
            height=650
        )
        chartSPoints = alt.Chart(data_list).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d') # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'Position:Q',
                scale=alt.Scale(domain=[maxNumberPos, 0])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'Position']
            # Aggiungi tooltip interattivi
        )
        chartS=chartS+chartSPoints
        #chartS = chartS.interactive()
        st.altair_chart(chartS, use_container_width=True)

    # ---------------------------------------------------------------

    #if (typeOfSession == 'R'):
        #NameSession = "Race"
    #elif typeOfSession == 'test':
        #NameSession = "test"
    #else:
        #NameSession = "FreePractice"

    #plt.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} - {drivers}")

    #Functions.savePlotInFile(plt, nameRace, yearRace,"\\"+NameSession+"\\" +str(typeOfSession)+"_PaceStint" + str(drivers), str(NameSession))
    return fig