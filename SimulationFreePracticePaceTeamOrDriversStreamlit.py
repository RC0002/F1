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

    data_list_Soft = None
    data_list_Medium= None
    data_list_Hard = None
    data_list_Wet = None
    data_list_Inter = None
    colors = []
    driversForColor = []
    maxNLap = 0
    minLapTime = 10000
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
        laps = race.laps.pick_driver(d).pick_accurate()
        if (laps.LapNumber.values.size > 0):
            #print(laps.LapNumber.size)
            numStint = laps[laps["LapNumber"] == laps.LapNumber.values[laps.LapNumber.values.size-1]].iloc[0].Stint
            for i in range(0,int(numStint)):
                #print(i)
                #aggiungo i colori per il print del grafico
                driversForColor.append(d + "" + str(i + 1))
                colors.append(color)

                #We are only analyzing stint 1, so select that one
                l = laps.loc[laps['Stint'] == i+1]

                l['RaceLapNumber'] = l['LapNumber'] - 1

                tmp=laps.loc[laps['Stint'] == i+1]
                linestyle = '-' if team not in visualized_teams else ':'
                try:
                    tmp = tmp.drop(tmp.loc[tmp['LapTime'] >= (l.pick_fastest(d).get("LapTime") + secondiDaConsiderare)].index).LapNumber.values.size
                except:
                    tmp=0
                if(tmp>2):
                    fig.suptitle(" Stint comparison")
                    #print(l.pick_fastest(d).get("LapTime") + '00:00:8.000000')
                    if l.Compound.max() != 'WET' and l.Compound.max() != 'INTERMEDIATE':
                        l.drop(l.loc[l['LapTime'] >= (l.pick_fastest(d).get("LapTime") + secondiDaConsiderare)].index,inplace=True)

                    if l.Compound.max() == 'SOFT':
                        #if l.FreshTyre.max():
                            #ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='o',label=d, linestyle=linestyle)
                        #else:
                            #ax[0].plot(l['RaceLapNumber'], l['LapTime'],color=color, markerfacecolor='r',marker='D', label=d, linestyle=linestyle)

                        # ---------------------------------------------------------------
                        l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                        chart_dataSoft = pd.DataFrame({
                            "Driver": d + "" +str(i + 1) ,
                            "RaceLapNumber": l['RaceLapNumber'],
                            "LapTime": l['LapTime_seconds'],
                            "Stint": i + 1,
                            "Compound": l.Compound.max(),
                            "isFreshTyre": l.FreshTyre.max()
                        })
                        if(data_list_Soft is None):
                            data_list_Soft = chart_dataSoft
                        else:
                            data_list_Soft = pd.concat([chart_dataSoft,data_list_Soft], ignore_index=True)

                        # ---------------------------------------------------------------

                    elif l.Compound.max() == 'MEDIUM':
                        #if l.FreshTyre.max():
                            #ax[1].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='o', label=d, linestyle=linestyle)
                        #else:
                            #ax[1].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='y',marker='D', label=d, linestyle=linestyle)

                        # ---------------------------------------------------------------
                        l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                        chart_dataMedium = pd.DataFrame({
                            "Driver" : d + "" +str(i + 1),
                            "RaceLapNumber": l['RaceLapNumber'],
                            "LapTime": l['LapTime_seconds'],  # Ensure it's numeric
                            "Stint": i + 1,
                            "Compound": l.Compound.max(),
                            "isFreshTyre": l.FreshTyre.max()
                        })

                        if (data_list_Medium is None):
                            data_list_Medium = chart_dataMedium
                        else:
                            data_list_Medium = pd.concat([chart_dataMedium, data_list_Medium], ignore_index=True)
                        # ---------------------------------------------------------------
                    elif l.Compound.max() == 'HARD':
                        #if l.FreshTyre.max():
                            #ax[2].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='o', label=d, linestyle=linestyle)
                        #else:
                            #ax[2].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='w',marker='D', label=d, linestyle=linestyle)

                        # ---------------------------------------------------------------
                        l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                        chart_dataHard = pd.DataFrame({
                            "Driver": d + "" +str(i + 1),
                            "RaceLapNumber": l['RaceLapNumber'],
                            "LapTime": l['LapTime_seconds'],  # Ensure it's numeric
                            "Stint": i + 1,
                            "Compound": l.Compound.max(),
                            "isFreshTyre": l.FreshTyre.max()
                        })
                        if (data_list_Hard is None):
                            data_list_Hard = chart_dataHard
                        else:
                            data_list_Hard = pd.concat([chart_dataHard , data_list_Hard], ignore_index=True)
                        # ---------------------------------------------------------------

                    elif l.Compound.max() == 'WET':
                        #if l.FreshTyre.max():
                            #ax[3].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='o', label=d)
                        #else:
                            #ax[3].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='b',marker='D', label=d)

                        l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                        chart_dataWet = pd.DataFrame({
                            "Driver": d + "" + str(i + 1),
                            "RaceLapNumber": l['RaceLapNumber'],
                            "LapTime": l['LapTime_seconds'],  # Ensure it's numeric
                            "Stint": i + 1,
                            "Compound": l.Compound.max(),
                            "isFreshTyre": l.FreshTyre.max()
                        })
                        if (data_list_Wet is None):
                            data_list_Wet = chart_dataWet
                        else:
                            data_list_Wet = pd.concat([chart_dataWet, data_list_Wet], ignore_index=True)
                    elif l.Compound.max() == 'INTERMEDIATE':
                        #if l.FreshTyre.max():
                            #ax[4].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='o', label=d)
                        #else:
                            #ax[4].plot(l['RaceLapNumber'], l['LapTime'], color=color, markerfacecolor='g',marker='D', label=d)

                        l['LapTime_seconds'] = l['LapTime'].dt.total_seconds()  # Converts to seconds
                        chart_dataInter = pd.DataFrame({
                            "Driver": d + "" + str(i + 1),
                            "RaceLapNumber": l['RaceLapNumber'],
                            "LapTime": l['LapTime_seconds'],  # Ensure it's numeric
                            "Stint": i + 1,
                            "Compound": l.Compound.max(),
                            "isFreshTyre": l.FreshTyre.max()
                        })
                        if (data_list_Inter is None):
                            data_list_Inter = chart_dataInter
                        else:
                            data_list_Inter = pd.concat([chart_dataInter, data_list_Inter], ignore_index=True)


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
                    if (l['LapTime_seconds'].max() > maxLapTime):
                        maxLapTime = l['LapTime_seconds'].max()
                    if (l['LapTime_seconds'].min() < minLapTime):
                        minLapTime = l['LapTime_seconds'].min()



        visualized_teams.append(team)

    # ---------------------------------------------------------------
    # Creazione di un grafico con Altair
    # Crea il grafico con Altair

    if data_list_Soft is not None:
        chartS = alt.Chart(data_list_Soft).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime','Stint', "Compound" ,"isFreshTyre"]  # Aggiungi tooltip interattivi
        ).properties(
            title='Soft',  # Imposta il titolo del grafico
            width=600,
            height=400
        )
        chartSPoints = alt.Chart(data_list_Soft).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime', 'Stint', "Compound", "isFreshTyre"]
            # Aggiungi tooltip interattivi
        )
        chartS=chartS+chartSPoints
        chartS = chartS.interactive()
        st.altair_chart(chartS, use_container_width=True)
    if data_list_Medium is not None:
        chartM = alt.Chart(data_list_Medium).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime','Stint', "Compound" ,"isFreshTyre"]  # Aggiungi tooltip interattivi
        ).properties(
            title='Medium',
            width=600,
            height=400
        )
        chartMPoints = alt.Chart(data_list_Medium).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d')#axis=alt.Axis(tickMinStep=1)  # Imposta la scala per l'asse X

            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime', 'Stint', "Compound", "isFreshTyre"]
            # Aggiungi tooltip interattivi
        )
        chartM = chartMPoints + chartM
        chartM = chartM.interactive()
        st.altair_chart(chartM, use_container_width=True)
    if data_list_Hard is not None:
        chartH = alt.Chart(data_list_Hard).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime','Stint', "Compound" ,"isFreshTyre"]  # Aggiungi tooltip interattivi
        ).properties(
            title='Hard',
            width=600,
            height=400
        )
        chartHPoints = alt.Chart(data_list_Hard).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime', 'Stint', "Compound", "isFreshTyre"]
            # Aggiungi tooltip interattivi
        )
        chartH=chartHPoints+chartH
        chartH = chartH.interactive()
        st.altair_chart(chartH, use_container_width=True)
    if data_list_Wet is not None:
        chartW = alt.Chart(data_list_Wet).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime','Stint', "Compound" ,"isFreshTyre"]  # Aggiungi tooltip interattivi
        ).properties(
            title='Wet',
            width=600,
            height=400
        )
        chartWPoints = alt.Chart(data_list_Wet).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime', 'Stint', "Compound", "isFreshTyre"]
            # Aggiungi tooltip interattivi
        )
        chartW=chartWPoints+chartW
        chartW = chartW.interactive()
        st.altair_chart(chartW, use_container_width=True)
    if data_list_Inter is not None:
        chartI = alt.Chart(data_list_Inter).mark_line().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(tickMinStep=1, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N',legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime','Stint', "Compound" ,"isFreshTyre"]  # Aggiungi tooltip interattivi
        ).properties(
            title='Inter',
            width=600,
            height=400
        )
        chartIPoints = alt.Chart(data_list_Inter).mark_circle().encode(
            x=alt.X(
                'RaceLapNumber:Q',
                scale=alt.Scale(domain=[0, maxNLap]), axis=alt.Axis(grid=False, format='d')  # Imposta la scala per l'asse X
            ),
            y=alt.Y(
                'LapTime:Q',
                scale=alt.Scale(domain=[minLapTime, maxLapTime])  # Imposta la scala per l'asse Y
            ),
            color=alt.Color(
                'Driver:N', legend=None,
                scale=alt.Scale(
                    domain=driversForColor,  # Valori univoci
                    range=colors  # Colori associati
                )),
            tooltip=['Driver', 'RaceLapNumber', 'LapTime', 'Stint', "Compound", "isFreshTyre"]
            # Aggiungi tooltip interattivi
        )
        chartI=chartIPoints+chartI
        chartI = chartI.interactive()
        st.altair_chart(chartI, use_container_width=True)
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