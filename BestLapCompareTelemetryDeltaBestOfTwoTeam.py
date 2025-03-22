import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

import Functions


# Enable the cache by providing the name of the cache folder
#ff1.Cache.enable_cache('cache')

def execute(nameRace,yearRace,team1,team2,typeOfSession):

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


    quali = ff1.get_session(yearRace, nameRace,typeOfSession)
    quali.load() # This is new with Fastf1 v.2.2

    # This is how it used to be:
    # laps = quali.load_laps(with_telemetry=True)

    #ottiene il miglior pilota dei due team
    driver_1 = Functions.returnBestDriverOnTeam(team1,quali)
    driver_2 = Functions.returnBestDriverOnTeam(team2,quali)

    # Laps can now be accessed through the .laps object coming from the session
    laps_driver_1 = quali.laps.pick_driver(driver_1)
    laps_driver_2 = quali.laps.pick_driver(driver_2)

    # Select the fastest lap
    fastest_driver_1 = laps_driver_1.pick_fastest()
    fastest_driver_2 = laps_driver_2.pick_fastest()

    # Retrieve the telemetry and add the distance column
    telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
    telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

    # Make sure whe know the team name for coloring
    team_driver_1 = fastest_driver_1['Team']
    team_driver_2 = fastest_driver_2['Team']


    # Extract the delta time
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)

    plot_size = [21, 9]
    plot_title = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} VS {driver_2}"
    plot_ratios = [1, 3, 2, 1, 1, 2, 1]
    #plot_filename = plot_title.replace(" ", "") + ".png"


    # Make plot a bit bigger
    plt.rcParams['figure.figsize'] = plot_size

    # Create subplots with different sizes
    fig, ax = plt.subplots(7)
    fig.suptitle(plot_title)
    ax[0].subtitle = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} VS {driver_2}"
    ax[0].get_xaxis().set_visible(False)

    # Set the plot title
    #ax[0].title.set_text(plot_title)

    # Delta line
    ax[0].plot(ref_tel['Distance'], delta_time,linewidth=0.9,color='grey')
    ax[0].axhline(0,linewidth=0.2,color="yellow")
    ax[0].set(ylabel=f"Gap to {driver_2} (s)")
    ax[0].grid(linewidth=0.09, color="grey")
    ax[0].xaxis.grid(False, 'minor')
    ax[0].yaxis.grid(False, 'minor')
    ax[0].spines[['right', 'top']].set_visible(False)

    # Speed trace
    ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[1].set(ylabel='Speed')
    ax[1].legend(loc="lower right")
    ax[1].get_xaxis().set_visible(False)
    #ax[1].get_yaxis().set_visible(False)
    ax[1].grid(linewidth=0.09, color="grey")
    ax[1].xaxis.grid(False, 'minor')
    ax[1].yaxis.grid(False, 'minor')
    ax[1].spines[['right', 'top']].set_visible(False)

    # Throttle trace
    ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[2].set(ylabel='Throttle')
    ax[2].get_xaxis().set_visible(False)
    #ax[2].get_yaxis().set_visible(False)
    ax[2].grid(linewidth=0.09, color="grey")
    ax[2].xaxis.grid(False, 'minor')
    ax[2].yaxis.grid(False, 'minor')
    ax[2].spines[['right', 'top']].set_visible(False)

    # Brake trace
    ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[3].set(ylabel='Brake')
    ax[3].get_xaxis().set_visible(False)
    #ax[3].get_yaxis().set_visible(False)
    ax[3].grid(linewidth=0.09, color="grey")
    ax[3].xaxis.grid(False, 'minor')
    ax[3].yaxis.grid(False, 'minor')
    ax[3].spines[['right', 'top']].set_visible(False)

    # Gear trace
    ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[4].set(ylabel='Gear')
    ax[4].get_xaxis().set_visible(False)
    #ax[4].get_yaxis().set_visible(False)
    ax[4].grid(linewidth=0.09, color="grey")
    ax[4].xaxis.grid(False, 'minor')
    ax[4].yaxis.grid(False, 'minor')
    ax[4].spines[['right', 'top']].set_visible(False)

    # RPM trace
    ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[5].set(ylabel='RPM')
    ax[5].get_xaxis().set_visible(False)
    #ax[5].get_yaxis().set_visible(False)
    ax[5].grid(linewidth=0.09, color="grey")
    ax[5].xaxis.grid(False, 'minor')
    ax[5].yaxis.grid(False, 'minor')
    ax[5].spines[['right', 'top']].set_visible(False)

    # DRS trace
    ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1,
               color=ff1.plotting.team_color(team_driver_1),linewidth=0.9)
    ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2,
               color=ff1.plotting.team_color(team_driver_2),linewidth=0.9)
    ax[6].set(ylabel='DRS')
    ax[6].set(xlabel='Lap distance (meters)')
    ax[6].get_xaxis().set_visible(False)
    #ax[6].get_yaxis().set_visible(False)
    ax[6].grid(linewidth=0.09, color="grey")
    ax[6].xaxis.grid(False, 'minor')
    ax[6].yaxis.grid(False, 'minor')
    ax[6].spines[['right', 'top']].set_visible(False)

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for a in ax.flat:
        a.label_outer()

    if(typeOfSession == 'Q'):
        NameSession = "Qualifying"
    else:
        NameSession = "FreePractice"


    Functions.savePlotInFile(plt,nameRace,yearRace,"\\"+NameSession+"\\" +typeOfSession+"_Telemetry" + driver_1 + "vs" + driver_2,NameSession)
    print("Fine")