import fastf1 as ff1
from fastf1 import plotting

import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import cm

import numpy as np

import Functions


# Enable the cache
#ff1.Cache.enable_cache('cache/')

def execute(nameRace,yearRace,teams):

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

    # Get rid of an error
    pd.options.mode.chained_assignment = None

    # Load the session data
    race = ff1.get_session(yearRace, nameRace, 'R')
    race.load(telemetry=False)
    # Get the laps
    laps = race.laps

    # Convert laptimes to seconds
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # To get accurate laps only, we exclude in- and outlaps
    laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]

    # Also, we remove outliers since those don't represent the racepace,
    # using the Inter-Quartile Range (IQR) proximity rule
    q75, q25 = laps['LapTimeSeconds'].quantile(0.75), laps['LapTimeSeconds'].quantile(0.25)

    intr_qr = q75 - q25

    laptime_max = q75 + (1.5 * intr_qr) # IQR proximity rule: Max = q75 + 1,5 * IQR
    laptime_min = q25 - (1.5 * intr_qr) # IQR proximity rule: Min = q25 + 1,5 * IQR

    laps.loc[laps['LapTimeSeconds'] < laptime_min, 'LapTimeSeconds'] = np.nan
    laps.loc[laps['LapTimeSeconds'] > laptime_max, 'LapTimeSeconds'] = np.nan

    #appende i nomi dei piloti che vogliamo stampare
    drivers_to_visualize=[]
    for i in range(len(race.results.index)):
        if race.results.iloc[i].get("TeamName") in teams:
            drivers_to_visualize.append(race.results.iloc[i].get("Abbreviation"))

    #drivers_to_visualize = ['VER', 'PER', 'LEC','HAM','RUS','SAI']
    #print(drivers_to_visualize)

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    # Make plot a bit bigger
    plt.rcParams['figure.figsize'] = [16, 9]

    # Create 2 subplots (1 for the boxplot, 1 for the lap-by-lap comparison)
    fig, ax = plt.subplots(2)
    #ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))

    ##############################
    #
    # Boxplot for average racepace
    #
    ##############################
    laptimes = [laps.pick_driver(x)['LapTimeSeconds'].dropna() for x in drivers_to_visualize]

    ax[0].boxplot(laptimes, labels=drivers_to_visualize)

    fig.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} ")
    ax[0].set(ylabel='Laptime (s)')
    ax[0].grid(linewidth=0.09, color="grey")
    ax[0].xaxis.grid(False, 'minor')
    ax[0].yaxis.grid(False, 'minor')
    ax[0].spines[['right', 'top']].set_visible(False)

    ##############################
    #
    # Lap-by-lap racepace comparison
    #
    ##############################
    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    for driver in drivers_to_visualize:
        driver_laps = laps.pick_drivers(driver)[['LapNumber', 'LapTimeSeconds', 'Team']]

        # Select all the laps from that driver
        driver_laps = driver_laps.dropna()

        # Extract the team for coloring purposes
        team = pd.unique(driver_laps['Team'])

        if not driver_laps.empty:

            # X-coordinate is the lap number
            x = driver_laps['LapNumber']

            # Y-coordinate a smoothed line between all the laptimes
            poly = np.polyfit(driver_laps['LapNumber'], driver_laps['LapTimeSeconds'], 5)
            y_poly = np.poly1d(poly)(driver_laps['LapNumber'])

            # Make sure that two teammates don't get the same line style
            linestyle = '-' if team not in visualized_teams else ':'

            colorq=ff1.plotting.get_team_color(team[0],race, colormap='official', exact_match=False)

            if (colorq == '#ffffff'):
                colorq = '#ccdbe4'
            # Plot the data
            ax[1].plot(x, y_poly, label=driver, color=colorq, linestyle=linestyle)

            # Include scatterplot (individual laptimes)
            # y = driver_laps['LapTimeSeconds']
            # scatter_marker = 'o' if team not in visualized_teams else '^'
            # ax[1].scatter(x, y, label=driver, color=ff1.plotting.team_color(team), marker=scatter_marker)

            # Append labels
            ax[1].set(ylabel='Laptime (s)')
            ax[1].set(xlabel='Lap')
            ax[1].grid(linewidth=0.09, color="grey")
            ax[1].xaxis.grid(False, 'minor')
            ax[1].yaxis.grid(False, 'minor')
            ax[1].spines[['right', 'top']].set_visible(False)

            # Set title
            ax[1].set_title('Smoothed lap-by-lap racepace')

            # Generate legend
            ax[1].legend()

            # Add the team to the visualized teams variable so that the next time the linestyle will be different
            visualized_teams.append(team)

        #plt.savefig('racepace_comparison.png', dpi=300)

    Functions.savePlotInFile(plt,nameRace,yearRace,"\Race\\" +"R_PaceInterBoxPlot " + str(teams),"Race")
    print("Fine")

def executeNoBoxPlot(nameRace,yearRace,teams):

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

    # Get rid of an error
    pd.options.mode.chained_assignment = None

    # Load the session data
    race = ff1.get_session(yearRace, nameRace, 'R')
    race.load(telemetry=True)
    # Get the laps
    laps = race.laps

    # Convert laptimes to seconds
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # To get accurate laps only, we exclude in- and outlaps
    laps = laps.loc[(laps['PitOutTime'].isnull() & laps['PitInTime'].isnull())]

    # Also, we remove outliers since those don't represent the racepace,
    # using the Inter-Quartile Range (IQR) proximity rule
    q75, q25 = laps['LapTimeSeconds'].quantile(0.75), laps['LapTimeSeconds'].quantile(0.25)

    intr_qr = q75 - q25

    laptime_max = q75 + (1.5 * intr_qr) # IQR proximity rule: Max = q75 + 1,5 * IQR
    laptime_min = q25 - (1.5 * intr_qr) # IQR proximity rule: Min = q25 + 1,5 * IQR

    laps.loc[laps['LapTimeSeconds'] < laptime_min, 'LapTimeSeconds'] = np.nan
    laps.loc[laps['LapTimeSeconds'] > laptime_max, 'LapTimeSeconds'] = np.nan

    #appende i nomi dei piloti che vogliamo stampare
    drivers_to_visualize=[]
    for i in range(len(race.results.index)):
        if race.results.iloc[i].get("TeamName") in teams:
            drivers_to_visualize.append(race.results.iloc[i].get("Abbreviation"))

    #drivers_to_visualize = ['VER', 'PER', 'LEC','HAM','RUS','SAI']
    #print(drivers_to_visualize)

    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    # Make plot a bit bigger
    plt.rcParams['figure.figsize'] = [16, 9]

    # Create 2 subplots (1 for the boxplot, 1 for the lap-by-lap comparison)
    fig, ax = plt.subplots(1)
    ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))

    ##############################
    #
    # Boxplot for average racepace
    #
    ##############################
    laptimes = [laps.pick_driver(x)['LapTimeSeconds'].dropna() for x in drivers_to_visualize]

    #ax[0].boxplot(laptimes, labels=drivers_to_visualize)

    fig.suptitle(f"{race.event.year} {race.event.EventName} - {race.name} ")
    #ax[0].set(ylabel='Laptime (s)')
    #ax[0].grid(linewidth=0.09, color="grey")
    #ax[0].xaxis.grid(False, 'minor')
    #ax[0].yaxis.grid(False, 'minor')
    #ax[0].spines[['right', 'top']].set_visible(False)

    ##############################
    #
    # Lap-by-lap racepace comparison
    #
    ##############################
    # To make sure we won't get any equally styled lines when comparing teammates
    visualized_teams = []

    for driver in drivers_to_visualize:
        driver_laps = laps.pick_driver(driver)[['LapNumber', 'LapTimeSeconds', 'Team']]

        # Select all the laps from that driver
        driver_laps = driver_laps.dropna()

        # Extract the team for coloring purploses
        team = pd.unique(driver_laps['Team'])

        if not driver_laps.empty:
            # X-coordinate is the lap number
            x = driver_laps['LapNumber']

            # Y-coordinate a smoothed line between all the laptimes
            poly = np.polyfit(driver_laps['LapNumber'], driver_laps['LapTimeSeconds'], 5)
            y_poly = np.poly1d(poly)(driver_laps['LapNumber'])

            # Make sure that two teammates don't get the same line style
            linestyle = '-' if team not in visualized_teams else ':'

            colorq=ff1.plotting.get_team_color(team[0],race, colormap='official', exact_match=False)
            if (colorq == '#ffffff'):
                colorq = '#ccdbe4'
            # Plot the data
            ax.plot(x, y_poly, label=driver, color=colorq, linestyle=linestyle)

            # Include scatterplot (individual laptimes)
            # y = driver_laps['LapTimeSeconds']
            # scatter_marker = 'o' if team not in visualized_teams else '^'
            # ax[1].scatter(x, y, label=driver, color=ff1.plotting.team_color(team), marker=scatter_marker)

            # Append labels
            ax.set(ylabel='Laptime (s)')
            ax.set(xlabel='Lap')
            ax.grid(linewidth=0.09, color="grey")
            ax.xaxis.grid(False, 'minor')
            ax.yaxis.grid(False, 'minor')
            ax.spines[['right', 'top']].set_visible(False)

            # Set title
            #ax[0].set_title('Smoothed lap-by-lap racepace')

            # Generate legend
            ax.legend()

            # Add the team to the visualized teams variable so that the next time the linestyle will be different
            visualized_teams.append(team)

            #plt.savefig('racepace_comparison.png', dpi=300)

    Functions.savePlotInFile(plt,nameRace,yearRace,"\Race\\" +"R_PaceInter " + str(teams),"Race")
    print("Fine")