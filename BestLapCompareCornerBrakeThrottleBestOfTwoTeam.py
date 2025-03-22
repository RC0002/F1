import os

import numpy as np
import pandas as pd

import fastf1 as ff1
from fastf1 import plotting

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import Functions


# Enable the cache
#ff1.Cache.enable_cache('cache')

#nameRace nome della gara che verra' usato per nominare la cartella
#yearRace anno della gara che verra' usato per nominare la cartella
#team del primo pilota
#team del secondo pilota
#distance_min distance_max distanza per la regione della curva da analizzare


def execute(nameRace,yearRace,team1,team2,distance_min,distance_max,typeOfSession,curvaNum):
    #Load the session data
    #quali = ff1.get_session(2021, 'Spain', 'Q')
    quali = ff1.get_session(yearRace, nameRace, typeOfSession)
    quali.load(telemetry=True)
    # Get the laps
    laps = quali.laps

    # Setting parameters
    driver_1 = Functions.returnBestDriverOnTeam(team1, quali)
    driver_2 = Functions.returnBestDriverOnTeam(team2, quali)


    # Extracting the laps
    laps_driver_1 = laps.pick_drivers(driver_1)
    laps_driver_2 = laps.pick_drivers(driver_2)

    telemetry_driver_1 = laps_driver_1.pick_fastest().get_car_data().add_distance()
    telemetry_driver_2 = laps_driver_2.pick_fastest().get_car_data().add_distance()

    # Identifying the team for coloring later on
    team_driver_1 = laps_driver_1.reset_index().loc[0, 'Team']
    team_driver_2 = laps_driver_2.reset_index().loc[0, 'Team']


    # Assigning labels to what the drivers are currently doing
    telemetry_driver_1.loc[telemetry_driver_1['Brake'] > 0, 'CurrentAction'] = 'Brake'
    telemetry_driver_1.loc[telemetry_driver_1['Throttle'] == 100, 'CurrentAction'] = 'Full Throttle'
    telemetry_driver_1.loc[(telemetry_driver_1['Brake'] == 0) & (telemetry_driver_1['Throttle'] < 100), 'CurrentAction'] = 'Cornering'

    telemetry_driver_2.loc[telemetry_driver_2['Brake'] > 0, 'CurrentAction'] = 'Brake'
    telemetry_driver_2.loc[telemetry_driver_2['Throttle'] == 100, 'CurrentAction'] = 'Full Throttle'
    telemetry_driver_2.loc[(telemetry_driver_2['Brake'] == 0) & (telemetry_driver_2['Throttle'] < 100), 'CurrentAction'] = 'Cornering'

    # Numbering each unique action to identify changes, so that we can group later on
    telemetry_driver_1['ActionID'] = (telemetry_driver_1['CurrentAction'] != telemetry_driver_1['CurrentAction'].shift(1)).cumsum()
    telemetry_driver_2['ActionID'] = (telemetry_driver_2['CurrentAction'] != telemetry_driver_2['CurrentAction'].shift(1)).cumsum()

    # Identifying all unique actions
    actions_driver_1 = telemetry_driver_1[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()
    actions_driver_2 = telemetry_driver_2[['ActionID', 'CurrentAction', 'Distance']].groupby(['ActionID', 'CurrentAction']).max('Distance').reset_index()

    actions_driver_1['Driver'] = driver_1
    actions_driver_2['Driver'] = driver_2


    # Calculating the distance between each action, so that we know how long the bar should be
    actions_driver_1['DistanceDelta'] = actions_driver_1['Distance'] - actions_driver_1['Distance'].shift(1)
    actions_driver_1.loc[0, 'DistanceDelta'] = actions_driver_1.loc[0, 'Distance']

    actions_driver_2['DistanceDelta'] = actions_driver_2['Distance'] - actions_driver_2['Distance'].shift(1)
    actions_driver_2.loc[0, 'DistanceDelta'] = actions_driver_2.loc[0, 'Distance']

    # Merging together
    all_actions = actions_driver_1.append(actions_driver_2)


    # Calculating average speed
    avg_speed_driver_1 = np.mean(telemetry_driver_1['Speed'].loc[
        (telemetry_driver_1['Distance'] >= distance_min) &
            (telemetry_driver_1['Distance'] >= distance_max)
    ])


    avg_speed_driver_2 = np.mean(telemetry_driver_2['Speed'].loc[
        (telemetry_driver_2['Distance'] >= distance_min) &
            (telemetry_driver_2['Distance'] >= distance_max)
    ])

    if avg_speed_driver_1 > avg_speed_driver_2:
        speed_text = f"{driver_1} {round(avg_speed_driver_1 - avg_speed_driver_2,2)}km/h faster"
    else:
        speed_text = f"{driver_1} {round(avg_speed_driver_2 - avg_speed_driver_1,2)}km/h faster"

    ##############################
    #
    # Setting everything up
    #
    ##############################
    plt.rcParams["figure.figsize"] = [13, 10]
    plt.style.use('dark_background')
    plt.rcParams["figure.autolayout"] = True
    #plt.suptitle("Qualifica telemetry " + driver_1 + " e " + driver_2)
    plt.suptitle(f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} VS {driver_2}")

    telemetry_colors = {
        'Full Throttle': 'green',
        'Cornering': 'grey',
        'Brake': 'red',
    }

    fig, ax = plt.subplots(2)

    ##############################
    #
    # Lineplot for speed
    #
    ##############################
    ax[0].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1))
    ax[0].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2))

    # Speed difference
    ax[0].text(distance_min + 15, 200, speed_text, fontsize=15)

    ax[0].set(ylabel='Speed')
    ax[0].legend(loc="lower right")

    ##############################
    #
    # Horizontal barplot for telemetry
    #
    ##############################
    for driver in [driver_1, driver_2]:
        driver_actions = all_actions.loc[all_actions['Driver'] == driver]

        previous_action_end = 0
        for _, action in driver_actions.iterrows():
            ax[1].barh(
                [driver],
                action['DistanceDelta'],
                left=previous_action_end,
                color=telemetry_colors[action['CurrentAction']]
            )

            previous_action_end = previous_action_end + action['DistanceDelta']

    ##############################
    #
    # Styling of the plot
    #
    ##############################
    # Set x-label
    plt.xlabel('Distance')

    # Invert y-axis
    plt.gca().invert_yaxis()

    # Remove frame from plot
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['left'].set_visible(False)

    # Add legend
    labels = list(telemetry_colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=telemetry_colors[label]) for label in labels]
    ax[1].legend(handles, labels)

    # Zoom in on the specific part we want to see
    ax[0].set_xlim(distance_min, distance_max)
    ax[1].set_xlim(distance_min, distance_max)

    if(typeOfSession == 'Q'):
        NameSession = "Qualifying"
    else:
        NameSession = "FreePractice"

    dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici", str(yearRace) + "_" + nameRace)
    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici\\" + str(yearRace) + "_" + nameRace + "\\"+NameSession,"CornersAnalysis")
    if not os.path.exists(dir):
        os.mkdir(dir)

    # Save the plot
    Functions.savePlotInFile(plt, nameRace, yearRace,"\\"+NameSession+"\CornersAnalysis\\" +typeOfSession+"_Corner_"+str(curvaNum)+"_" + driver_1 + "vs" + driver_2, NameSession)
    print("Fine")

def getDistanceCorner(nameRace,yearRace,tipeOfSession):
    Corners=[]
    brake = False
    quali = ff1.get_session(yearRace, nameRace, tipeOfSession)
    quali.load(telemetry=True)
    # Get the laps
    laps = quali.laps
    driver = quali.results.iloc[0].get("Abbreviation")
    # Extracting the laps
    laps_driver= laps.pick_driver(driver)
    telemetry_driver = laps_driver.pick_fastest().get_car_data().add_distance()
    #print(telemetry_driver)

    start=telemetry_driver.iloc[0].Speed
    max=telemetry_driver.iloc[0].Speed
    for i in telemetry_driver.iterrows():
        #print(i[1].get("Brake"))
        if(i[1].get("Speed")>=max):
            max = i[1].get("Speed")
        if(i[1].get("Brake")==True and brake==False):
            brake = True
            Corners.append(i[1].get("Distance"))
        if(i[1].get("Brake") == False and brake == True):
            brake = False
    return Corners
    #print(max)

def getCornerReleeaseBrake(nameRace,yearRace,tipeOfSession):
    Corners=[]
    brake = False
    quali = ff1.get_session(yearRace, nameRace, tipeOfSession)
    quali.load(telemetry=True)
    # Get the laps
    laps = quali.laps
    driver = quali.results.iloc[0].get("Abbreviation")
    # Extracting the laps
    laps_driver= laps.pick_driver(driver)
    telemetry_driver = laps_driver.pick_fastest().get_car_data().add_distance()
    #print(telemetry_driver)

    start=telemetry_driver.iloc[0].Speed
    max=telemetry_driver.iloc[0].Speed
    for i in telemetry_driver.iterrows():
        #print(i[1].get("Brake"))
        if(i[1].get("Brake")==False and brake==True):
            brake = False
            Corners.append(i[1].get("Distance"))
        if(i[1].get("Brake") == True and brake == False):
            brake = True
    return Corners
    #print(max)