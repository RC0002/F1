import os
from datetime import datetime

import fastf1.events
from fastf1.core import Laps

import BestLapCompareSpeedAndDeltaBestOfTwoTeam
import BestLapCompareCornerBrakeThrottleBestOfTwoTeam
import BestLapCompareTelemetryDeltaBestOfTwoTeam
import Functions
import Plot_qualifying_results
import RacePaceAll
import RacePaceInterpolatoConGraficoMediaEVarianza
import fastf1 as ff1
import pandas as pd
import RacePaceTeamOrDrivers
import SimulationFreePracticePaceTeamOrDrivers
import DownloadGraphics

ff1.Cache.enable_cache('\\Users\comer\Documents\F1 Data\cache')

from fastf1.ergast import Ergast

exit = False

race = 'Bahrain'
yearRace = 2023

while exit==False:
    os.system('cls')
    print("MENU")
    print('1] Classifica')
    print('2] Scarica Grafici')
    print('3] Exit')

    sceltaMenu = int(input("Inserisci scelta: "))


    match sceltaMenu:
        case 1:

            ergast = Ergast()
            calendario = ergast.get_race_schedule(2019)

            # Convertire le colonne con date e ore in formato datetime
            print(calendario)


            os.system('cls')
            ergast = Ergast()
            anno_attuale = datetime.now().year
            standings = ergast.get_constructor_standings(anno_attuale)
            print(standings.content[0].to_string(index=False))
            if(not standings.description.empty):
                print('CLASSIFICA COSTRUTTORI MONDIALE F1 ' + str(anno_attuale) +'\n')
                print(standings.content[0][['constructorName', 'points', 'wins']])
            else:
                print('CLASSIFICA COSTRUTTORI MONDIALE F1 ' + str(anno_attuale-1) +'\n')
                standings = ergast.get_constructor_standings(anno_attuale-1)
                print(standings.content[0][['constructorName', 'points', 'wins']])
            input("\nEnter to exit")

        case 2:
            os.system('cls')
            DownloadGraphics.execute()
        case 3:
            exit = True


