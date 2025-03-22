"""Qualifying results overview
==============================

Plot the qualifying result with visualization the fastest times.
"""


import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import fastf1
import fastf1.plotting
from fastf1.core import Laps

import Functions


def execute(nameRace,yearRace,typeOfSession):

    # we only want support for timedelta plotting in this example
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    session = fastf1.get_session(yearRace, nameRace, typeOfSession)
    session.load()


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


    ##############################################################################
    # First, we need to get an array of all drivers.

    drivers = pd.unique(session.laps['Driver'])


    ##############################################################################
    # After that we'll get each drivers fastest lap, create a new laps object
    # from these laps, sort them by lap time and have pandas reindex them to
    # number them nicely by starting position.

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_drivers(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)


    ##############################################################################
    # The plot is nicer to look at and more easily understandable if we just plot
    # the time differences. Therefore we subtract the fastest lap time from all
    # other lap times.

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']


    ##############################################################################
    # We can take a quick look at the laps we have to check if everything
    # looks all right. For this, we'll just check the 'Driver', 'LapTime'
    # and 'LapTimeDelta' columns.

    #print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])


    ##############################################################################
    # Finally, we'll create a list of team colors per lap to color our plot.
    team_colors = list()
    for index, lap in fastest_laps.iterlaps():
        #print(type(lap['Team']))
        try:
            color = fastf1.plotting.team_color(lap['Team'])
            team_colors.append(color)
        except:
            print("Errore")


    ##############################################################################
    # Now, we can plot all the data

    fig, ax = plt.subplots()
    ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])

    # show fastest at the top
    ax.invert_yaxis()

    # draw vertical lines behind the bars
    #ax.set_axisbelow(True)
    #ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
    ax.grid(linewidth=0.09, color="grey")
    ax.xaxis.grid(False, 'minor')
    ax.yaxis.grid(False, 'minor')
    ax.spines[['right', 'top']].set_visible(False)
    # sphinx_gallery_defer_figures


    ##############################################################################
    # Finally, give the plot a meaningful title

    if (typeOfSession == 'R'):
        NameSession = "Race"
    elif typeOfSession == 'Q':
        NameSession = "Qualifying"
    else:
        NameSession = "FreePractice"

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

    plt.suptitle(f"{session.event['EventName']} {session.event.year} {NameSession}\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")



    Functions.savePlotInFile(plt, nameRace, yearRace, "\\" + NameSession + "\\"+ typeOfSession + "_Results", NameSession)
