import fastf1 as ff1
import numpy as np
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt, ticker
from numpy.core.defchararray import rsplit

import BestLapCompareCornerBrakeThrottleBestOfTwoTeam
import Functions

#nameRace nome della gara che verra' usato per nominare la cartella
#yearRace anno della gara che verra' usato per nominare la cartella
#team del primo pilota
#team del secondo pilota

def execute(nameRace,yearRace,team1,team2,team3,typeOfSession):

    ff1.Cache.enable_cache('\\Users\comer\Documents\F1 Data\cache')
    plotting.setup_mpl()

    session = ff1.get_session(yearRace, nameRace, typeOfSession)
    session.load()
    laps=session.laps

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


    #ottiene il miglior pilota dei due team
    driver_1 = Functions.returnBestDriverOnTeam(team1,session)
    driver_2 = Functions.returnBestDriverOnTeam(team2,session)
    driver_3 = Functions.returnBestDriverOnTeam(team3, session)

    team1DriverLap = laps.pick_drivers(driver_2).pick_fastest()
    team2DriverLap = laps.pick_drivers(driver_1).pick_fastest()
    team3DriverLap = laps.pick_drivers(driver_3).pick_fastest()

    Functions.getBestSpeed(team1DriverLap)

    delta_time, ref_tel, compare_tel = utils.delta_time(team2DriverLap, team1DriverLap)
    delta_time1, ref_tel1, compare_tel1 = utils.delta_time(team1DriverLap, team3DriverLap)
    # ham is reference, lec is compared

    if(typeOfSession == 'Q'):
        NameSession = "Qualifying"
    else:
        NameSession = "FreePractice"


    fig, ax = plt.subplots()
    ax = fig.add_axes((0.05, 0.05, 0.9, 0.9))

    # use telemetry returned by .delta_time for best accuracy,
    # this ensure the same applied interpolation and resampling
    ax.plot(ref_tel['Distance'], ref_tel['Speed'],color=plotting.get_team_color(team2DriverLap['Team'],session, colormap='official', exact_match=False),label=driver_1,linewidth=1)
    ax.plot(ref_tel1['Distance'], ref_tel1['Speed'], color=plotting.get_team_color(team1DriverLap['Team'],session, colormap='official', exact_match=False), label=driver_2,linewidth=1)
    ax.plot(compare_tel['Distance'], compare_tel['Speed'],color=plotting.get_team_color(team1DriverLap['Team'],session, colormap='official', exact_match=False),label=driver_2,linewidth=1)
    ax.plot(compare_tel1['Distance'], compare_tel1['Speed'], color=plotting.get_team_color(team3DriverLap['Team'],session, colormap='official', exact_match=False),label=driver_3, linewidth=1)

    color1 = plotting.get_team_color(team1DriverLap['Team'],session, colormap='official', exact_match=False)
    color2 = plotting.get_team_color(team2DriverLap['Team'],session, colormap='official', exact_match=False)
    color3 = plotting.get_team_color(team3DriverLap['Team'],session, colormap='official', exact_match=False)

    ax.legend(loc="lower right")
    plt.suptitle(f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2} VS {driver_3}")
    ax.grid(linewidth=0.01,color="grey")
    ax.set_xlabel('Metri',fontweight='bold')
    ax.set_ylabel('Velocita',fontweight='bold')

    ax.text(0.1, 1, "Top Speed: ",
          horizontalalignment='center',transform=ax.transAxes, verticalalignment='baseline')
    ax.text(0.1, 0.98, "\n" + driver_1 + "=" + str(Functions.getBestSpeed(team2DriverLap)),
          horizontalalignment='center',transform=ax.transAxes, verticalalignment='baseline',c=color2)
    ax.text(0.1, 0.96, "\n\n"+ driver_2 + "=" + str(Functions.getBestSpeed(team1DriverLap)),
          horizontalalignment='center',transform=ax.transAxes, verticalalignment='baseline',c=color1)
    ax.text(0.1, 0.94,"\n\n\n"+  driver_3 + "=" + str(Functions.getBestSpeed(team3DriverLap)),
          horizontalalignment='center',transform=ax.transAxes, verticalalignment='baseline',c=color3)

    ax.text(0.90, 0.98,
            driver_1 + " " + str(Functions.getBestSectors(team2DriverLap)) +'   '+Functions.getTyre(team2DriverLap),
            horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline',c=color2)
    ax.text(0.90, 0.96,
            driver_2 + " " + str(Functions.getBestSectors(team1DriverLap)) +'   '+Functions.getTyre(team1DriverLap),
            horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline',c=color1)
    ax.text(0.90, 0.94,
            driver_3 + " " + str(Functions.getBestSectors(team3DriverLap)) +'   '+Functions.getTyre(team3DriverLap),
            horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline',c=color3)



    ax.yaxis.set_ticks(np.arange(40, 350, 10))
    Points = BestLapCompareCornerBrakeThrottleBestOfTwoTeam.getCornerReleeaseBrake(nameRace, yearRace,typeOfSession)
    ax.xaxis.set_ticks(Points)
    ax.spines[['right','top']].set_visible(False)

    maxVel1, maxDis1, minVel1, minDis1 = Functions.getMaxEndMinSpeedDifferent(team1DriverLap)
    maxVel2, maxDis2, minVel2, minDis2 = Functions.getMaxEndMinSpeedDifferent(team2DriverLap)
    maxVel3, maxDis3, minVel3, minDis3 = Functions.getMaxEndMinSpeedDifferent(team3DriverLap)
    #print(team2DriverLap.index)


    ax.axis([0, maxDis1[-1], 0, 360])
    #print(len(maxVel1))
    #print(len(maxVel2))
    #print(len(maxVel3))

    #plt.text.set_color(plotting.team_color(team2DriverLap['Team']))
    for i in range(len(maxVel1)):
        ax.text(maxDis1[i], maxVel1[i], maxVel1[i],c=color1)

    for i in range(len(minVel1)-1):
        ax.text(minDis1[i], minVel1[i], minVel1[i],c=color1)

    #plt.text.set_color(plotting.team_color(team1DriverLap['Team']))
    for i in range(len(maxVel2)):
        ax.text(maxDis2[i], maxVel2[i], maxVel2[i],c=color2)

    for i in range(len(minVel2)-1):
        ax.text(minDis2[i], minVel2[i], minVel2[i],c=color2)

    #plt.text.set_color(plotting.team_color(team3DriverLap['Team']))
    for i in range(len(maxVel3)):
        ax.text(maxDis3[i], maxVel3[i], maxVel3[i],c=color3)

    for i in range(len(minVel3)-1):
        ax.text(minDis3[i], minVel3[i], minVel3[i],c=color3)

    #ax.text(505, 322, 'Ciao')


    #print(len(maxVel1))
    #print(len(maxVel2))
    #print(len(maxVel3))
    color2 = ff1.plotting.get_team_color(team1DriverLap['Team'],session, colormap='official', exact_match=False)     #team 1 e il driver2
    color1 = ff1.plotting.get_team_color(team2DriverLap['Team'],session, colormap='official', exact_match=False)
    color3 = ff1.plotting.get_team_color(team3DriverLap['Team'],session, colormap='official', exact_match=False)

    if(len(maxVel1) == len(maxVel2)==len(maxVel3)and len(minVel1) == len(minVel2)==len(minVel3)):
        difPil12max = 0
        difPil12min = 0
        difPil13max = 0
        difPil13min = 0
        difPil23max = 0
        difPil23min = 0
        for i in range(len(maxVel1)):
            difPil12max = difPil12max + (maxVel2[i]-maxVel1[i])
            difPil13max = difPil13max + (maxVel2[i] - maxVel3[i])
            difPil23max = difPil23max + (maxVel1[i] - maxVel3[i])

        for i in range(len(minVel1)):
            difPil12min = difPil12min + (minVel2[i]-minVel1[i])
            difPil13min = difPil13min + (minVel2[i] - minVel3[i])
            difPil23min = difPil23min + (minVel1[i] - minVel3[i])


        #print(driver_1)
        #print(maxVel2)
        #print(minVel2)
        #print(driver_2)
        #print(maxVel1)
        #print(minVel1)
        #print(driver_3)
        #print('dif 1-3max' + str(difPil13max))
        #print('dif 1-3min' + str(difPil13min))
        #print(maxVel3)
        #print(minVel3)

        ax.text(0.05, 0.06,driver_1 + "",horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        ax.text(0.08, 0.06, driver_2 , horizontalalignment='center', transform=ax.transAxes,verticalalignment='baseline', c=color2)

        if difPil12max>0:
            ax.text(0.06, 0.02,
                    "diff. Vel. max: "+str(difPil12max),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        else:
            ax.text(0.06, 0.02,
                    "diff. Vel. max: "+str(difPil12max+(2*-difPil12max)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color2)

        if difPil12min>0:
            ax.text(0.06, 0.04,
                    "diff. Vel. min: "+str(difPil12min),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        else:
            ax.text(0.06, 0.04,
                    "diff. Vel. min: "+str(difPil12min+(2*-difPil12min)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color2)

        ax.text(0.15, 0.06,driver_1 + "",horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        ax.text(0.18, 0.06, driver_3 , horizontalalignment='center', transform=ax.transAxes,verticalalignment='baseline', c=color3)

        if difPil13max>0:
            ax.text(0.16, 0.02,
                    "diff. Vel. max: "+str(difPil13max),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        else:
            ax.text(0.16, 0.02,
                    "diff. Vel. max: "+str(difPil13max+(2*-difPil13max)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color3)

        if difPil13min>0:
            ax.text(0.16, 0.04,
                    "diff. Vel. min: "+str(difPil13min),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color1)
        else:
            ax.text(0.16, 0.04,
                    "diff. Vel. min: "+str(difPil13min+(2*-difPil13min)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color3)

        ax.text(0.25, 0.06,driver_2 + "",horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color2)
        ax.text(0.28, 0.06, driver_3 , horizontalalignment='center', transform=ax.transAxes,verticalalignment='baseline', c=color3)

        if difPil23max>0:
            ax.text(0.26, 0.02,
                    "diff. Vel. max: "+str(difPil23max),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color2)
        else:
            ax.text(0.26, 0.02,
                    "diff. Vel. max: "+str(difPil23max+(2*-difPil23max)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color3)

        if difPil23min>0:
            ax.text(0.26, 0.04,
                    "diff. Vel. min: "+str(difPil23min),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color2)
        else:
            ax.text(0.26, 0.04,
                    "diff. Vel. min: "+str(difPil23min+(2*-difPil23min)),
                    horizontalalignment='center', transform=ax.transAxes, verticalalignment='baseline', c=color3)



    Functions.savePlotInFile(plt,nameRace,yearRace,"\\"+NameSession+"\\" +typeOfSession+"_Delta" + driver_2 + "vs" + driver_1+ "vs" + driver_3,NameSession)
    print("Fine")



    #twin = ax.twinx()
    #twin.plot(ref_tel['Distance'], delta_time, '--', color='white')
    #twin.set_ylabel("<-- Lec ahead | Ham ahead -->")
    #plt.show()
    return fig