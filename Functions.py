import base64
import json
from datetime import datetime, timedelta
import os
import pandas as pd
import fastf1
from fastf1.core import Laps
import streamlit as st


#plt plot da stampare
#nameRace nome della gara che verra' usato per nominare la cartella
#yearRace anno della gara che verra' usato per nominare la cartella
#path percorso

def savePlotInFile(plt,nameRace,yearRace,path,tipeOfSession):
    # vede se c'e' la cartella della gara e nel caso la crea
    dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici", str(yearRace) + "_" + nameRace)

    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = os.path.join("\\Users\comer\Documents\F1 Data\\", "Grafici\\" + str(yearRace) + "_" + nameRace + "", tipeOfSession)
    if not os.path.exists(dir):
        os.mkdir(dir)

    # salva il file il locale
    plt.savefig("\\Users\comer\Documents\F1 Data\Grafici\\" + str(yearRace) + "_" + nameRace + path,dpi=800)
    plt.close()

def returnBestDriverOnTeam(Team,session):
    drivers = pd.unique(session.laps['Driver'])

    list_fastest_laps = list()
    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_drivers(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)

    list_fastest_laps = list(filter(lambda x: x is not None, list_fastest_laps)) # rimuove eventuali valori null
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    for i in fastest_laps.iterrows():
        if(i[1].get("Team")==Team):
            return i[1].get("Driver")

def printImageChampNotStarted():
    # Aggiunta di uno stile CSS per centrare l'immagine
    st.markdown(
        """
        <style>
        .centered-image {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 75vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with open("Waiting.png", "rb") as img_file:
        image_base64 = base64.b64encode(img_file.read()).decode()
    # Div per centrare l'immagine
    st.markdown(
        f"""
                        <div class="centered-image">
                            <img src="data:image/jpeg;base64,{image_base64}" alt="Immagine centrata">
                        </div>
                        """,
        unsafe_allow_html=True
    )

def getDriverOfTheSession(anno_attuale, nameRace, sessionRace):
    session = fastf1.get_session(anno_attuale, nameRace, sessionRace)
    session.load(telemetry=True)
    drivers = pd.unique(session.results.Abbreviation.drop_duplicates())
    return drivers

def getTeamOfTheSession(anno_attuale, nameRace, sessionRace):
    session = fastf1.get_session(anno_attuale, nameRace, sessionRace)
    session.load(telemetry=True)
    return list(session.results.TeamName.drop_duplicates())

def plotDriverCompare(race,plt,session,ff1,driver1,driver2):
    Dd1 = race.laps.pick_driver(driver1).pick_accurate()     #driver 1
    Dd2 = race.laps.pick_driver(driver2).pick_accurate()     #driver 2
    fig, ax = plt.subplots()
    t1 = session.get_driver(driver1)['TeamName']
    t2 = session.get_driver(driver2)['TeamName']
    c1 = ff1.plotting.team_color(t1)
    c2 = ff1.plotting.team_color(t2)
    ax.plot(Dd1['LapNumber'], Dd1['LapTime'], color=c1,linestyle="dashed",label=driver1,linewidth=3)
    ax.plot(Dd2['LapNumber'], Dd2['LapTime'], color=c2,linestyle="solid",label=driver2,linewidth=3)
    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")
    ax.legend(loc="upper center")

def getTeams(results):
    return list(set(results.TeamName.values))

def get_driversFromTeam(team,results):
    return list(results.Abbreviation[results.TeamName==team])

def getRacePerYear(year):
    fastf1.get_event_schedule(year).Country.values
    return fastf1.get_event_schedule(year).Country.values

def getEventNamePerYear(year):
    return fastf1.get_event_schedule(year)["EventName"]#EventName

def getEventNamePerYearBeforeSysdate(year):
    calendario = fastf1.get_event_schedule(year)
    calendario['EventDate'] = pd.to_datetime(calendario['EventDate'].dt.strftime('%Y-%m-%d'))
    # st.write(type(calendario[['raceName', 'raceDate']]))
    oggi = datetime.today() + timedelta(days=3)
    # Filtriamo solo gli eventi già passati
    eventi_passati = calendario[calendario["EventDate"] <= oggi]
    eventi_passati = eventi_passati.sort_values(by="EventDate", ascending=False)
    return eventi_passati["EventName"]

def getEventInformationPerYearAfterSysdate(year):
    calendario = fastf1.get_event_schedule(year)
    calendario['EventDate'] = pd.to_datetime(calendario['EventDate'].dt.strftime('%Y-%m-%d'))
    # st.write(type(calendario[['raceName', 'raceDate']]))
    oggi = datetime.today()
    # Filtriamo solo gli eventi già passati
    eventi_passati = calendario[calendario["EventDate"] >= oggi]
    eventi_passati = eventi_passati.sort_values(by="EventDate", ascending=True)
    return eventi_passati

def getDriverDefault():
    try:
        with open("driverDefault.json", "r") as json_file:
            driver_riaperto = json.load(json_file)
    except FileNotFoundError:
        driver_riaperto = []

    return driver_riaperto

def getTeamDefault():
    try:
        with open("teamDefault.json", "r") as json_file:
            team_riaperto = json.load(json_file)
    except FileNotFoundError:
        team_riaperto = []

    return team_riaperto

def getEventPerYear(year):
    return fastf1.get_event_schedule(year)

def getBestSpeed(lap):
    telemetry=lap.get_car_data()
    max=telemetry.iloc[0].Speed
    for i in telemetry.iterrows():
        #print(i[1].get("Brake"))
        if(i[1].get("Speed")>=max):
            max = i[1].get("Speed")
    return max

def getBestSectors(lap):
    #print(lap)
    tmp = str(lap.Sector1Time).rsplit(':')
    tmp1 = str(lap.Sector2Time).rsplit(':')
    tmp2 = str(lap.Sector3Time).rsplit(':')
    return tmp[1]+':'+tmp[2][:-3]+' | '+tmp1[1]+':'+tmp1[2][:-3]+' | '+tmp2[1]+':'+tmp2[2][:-3]

def getTyre(lap):
    return  str(lap.Compound)

def getMaxEndMinSpeed(lap):
    telemetry=lap.get_car_data().add_distance()
    max=0
    distMax=0
    min=350
    distMin=0
    disable = False
    maxVel=[]
    maxDis=[]
    minVel=[]
    minDis=[]
    #telemetry.iloc[0].Speed
    for i in telemetry.iterrows():
        #print(i[1].get("Brake"))
        #print(i[1].get("Speed"))
        #print("a max" + str(max) + "a min" + str(min))
        #print(i[1].get("Throttle"))
        if(i[1].get("Speed")>=max):
            max = i[1].get("Speed")
            distMax = i[1].get("Distance")
            #print("a max" + str(max) + "a min" + str(min))
        if(i[1].get("Speed")<=min):
            min = i[1].get("Speed")
            distMin = i[1].get("Distance")
            #print("a max" + str(max) + "a min" + str(min))
        if ((i[1].get("Brake") == True and disable == False and float(i[1].get("Throttle"))<50) or (i[1].get("Brake") == False and float(i[1].get("Throttle"))<50 and disable == False)):
            maxVel.append(max)
            maxDis.append(distMax)
            min=350
            disable=True
            #print('-------------------------------------------------------'+str(max))
            #print(max)
            #print(maxDis)
        if (i[1].get("Brake") == False and disable == True and float(i[1].get("Throttle"))>50 and i[1].get("Speed")>150):
            minVel.append(min)
            minDis.append(distMin)
            max=0
            disable=False
            #print('-------------------------------------------------------'+str(min))
            #print(minDis)
        #print(i[1].get("Speed"))
        #print(i[1].get("Throttle"))
    print(i[1].index)

    #print(maxDis,maxVel,minDis,minVel)
    return maxVel,maxDis,minVel,minDis


def getMaxEndMinSpeedDifferent(lap):
    telemetry=lap.get_car_data().add_distance()
    max=0
    distMax=0
    min=350
    distMin=0
    disable = True
    maxVel=[]
    maxDis=[]
    minVel=[]
    minDis=[]
    #telemetry.iloc[0].Speed
    for i in telemetry.iterrows():
        #print(i[1].get("Brake"))
        #print(i[1].get("Speed"))
        #print("a max" + str(max) + "a min" + str(min))
        #print(i[1].get("Throttle"))
        if(i[1].get("Speed")>=max and disable==True):
            max = i[1].get("Speed")
            distMax = i[1].get("Distance")
            disable=True
            #print("a max" + str(max) + "a min" + str(min))
        if(i[1].get("Speed")<=min and disable==False):
            min = i[1].get("Speed")
            distMin = i[1].get("Distance")
            disable = False
            #print("a max" + str(max) + "a min" + str(min))
        if (i[1].get("Speed")<max-5 and disable==True):
            maxVel.append(max)
            maxDis.append(distMax)
            min=350
            disable=False
            #print('-------------------------------------------------------'+str(max))
            #print(max)
            #print(maxDis)
        if (i[1].get("Speed")>min+5 and disable==False):
            minVel.append(min)
            minDis.append(distMin)
            max=0
            disable=True
            #print('-------------------------------------------------------'+str(min))
            #print(minDis)
        #print(i[1].get("Speed"))
        #print(i[1].get("Throttle"))
    #print(i[1].index)

    #print(maxDis,maxVel,minDis,minVel)
    return maxVel,maxDis,minVel,minDis