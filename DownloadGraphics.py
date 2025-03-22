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

def execute():
    yearRace = int(input("Inserisci anno: "))
    # yearRace=2024
    print(Functions.getRacePerYear(yearRace))
    race = input("Seleziona gara: ")
    # race="United Arab Emirates"
    print("1] Free Practice")
    print("2] Qualifying")
    print("3] Race")
    print("0] All")
    selezione = int(input("Seleziona quale sessione: "))
    # selezione=0
    # Free Practice _____________________________________________________________________________________________________________________________________________________
    if selezione == 1 or selezione == 0:
        fp = 'FP2'

        if (selezione != 0):
            print("1] FP1")
            print("2] FP2")
            print("3] FP3")
            selezione1 = int(input("Selezionare prova libera: "))
            # selezione1=3
            if selezione1 == 1:
                fp = "FP1"
            elif selezione1 == 2:
                fp = "FP2"
            elif selezione1 == 3:
                fp = "FP3"

        BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", "Mercedes", fp)
        BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", "McLaren", fp)

        BestLapCompareTelemetryDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", fp)
        BestLapCompareTelemetryDeltaBestOfTwoTeam.execute(race, yearRace, "Mercedes", "Ferrari", fp)
        BestLapCompareTelemetryDeltaBestOfTwoTeam.execute(race, yearRace, "McLaren", "Ferrari", fp)

        SimulationFreePracticePaceTeamOrDrivers.executeSimulationStintOfSomeDrivers(race, yearRace,
                                                                                    ['LEC', 'VER', 'HAM', 'LAW', 'RUS',
                                                                                     'ANT', 'NOR', 'PIA'], fp,
                                                                                    '00:00:2.000000')
        Plot_qualifying_results.execute(race, yearRace, fp)
        exit = True

        '''
        BrakingPoints = BestLapCompareCornerBrakeThrottleBestOfTwoTeam.getDistanceCorner(race, yearRace,fp)
        print(BrakingPoints)
        curvaNum=1
        for b in BrakingPoints:
            BestLapCompareCornerBrakeThrottleBestOfTwoTeam.execute(race,yearRace,"Red Bull Racing","Ferrari",b-100,b+400,fp,curvaNum)
            BestLapCompareCornerBrakeThrottleBestOfTwoTeam.execute(race,yearRace,"Mercedes","Ferrari",b-100,b+400,fp,curvaNum)
            curvaNum = curvaNum + 1
        '''

    # qualifying ________________________________________________________________________________________________________________________________________________________
    if selezione == 2 or selezione == 0:
        BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", "Mercedes", 'Q')
        BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", "McLaren", 'Q')

        BestLapCompareTelemetryDeltaBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", 'Q')
        BestLapCompareTelemetryDeltaBestOfTwoTeam.execute(race, yearRace, "Mercedes", "Ferrari", 'Q')
        Plot_qualifying_results.execute(race, yearRace, 'Q')
        exit = True

    # Race ______________________________________________________________________________________________________________________________________________________________
    if selezione == 3 or selezione == 0:
        RacePaceInterpolatoConGraficoMediaEVarianza.execute(race, yearRace,
                                                            ['Mercedes', 'Ferrari', 'Red Bull Racing', 'McLaren'])
        # RacePaceInterpolatoConGraficoMediaEVarianza.execute(race,yearRace,['Mclaren','Alpine','Kick Sauber','RB','Haas F1 Team','Williams'])
        RacePaceInterpolatoConGraficoMediaEVarianza.executeNoBoxPlot(race, yearRace,
                                                                     ['Mercedes', 'Ferrari', 'Red Bull Racing',
                                                                      'McLaren'])
        # RacePaceInterpolatoConGraficoMediaEVarianza.executeNoBoxPlot(race, yearRace,['Mclaren', 'Alpine', 'Kick Sauber', 'RB','Haas F1 Team', 'Williams'])

        RacePaceTeamOrDrivers.executeStintDriverOrTeam(race, yearRace,
                                                       ['Mercedes', 'Ferrari', 'Red Bull Racing', 'McLaren']);
        RacePaceTeamOrDrivers.executeStintDriverOrTeam(race, yearRace, ['LEC', 'VER', 'HAM',
                                                                        'NOR'])  # conviene fare il migliore del team??

        RacePaceTeamOrDrivers.executeStintOfSomeDrivers(race, yearRace,
                                                        ['LEC', 'VER', 'HAM', 'LAW', 'RUS', 'ANT', 'NOR', 'PIA'])

        RacePaceAll.execute(race, yearRace)
        # RacePaceAll.executeCompareOfDriverSameTeam(race,yearRace)
        Plot_qualifying_results.execute(race, yearRace, 'R')
        exit = True

        '''
        BrakingPoints = BestLapCompareCornerBrakeThrottleBestOfTwoTeam.getDistanceCorner(race, yearRace,'Q')
        curvaNum = 1
        for b in BrakingPoints:
            BestLapCompareCornerBrakeThrottleBestOfTwoTeam.execute(race, yearRace, "Red Bull Racing", "Ferrari", b - 100,b + 400, 'Q', curvaNum)
            BestLapCompareCornerBrakeThrottleBestOfTwoTeam.execute(race, yearRace, "Mercedes", "Ferrari", b - 100, b + 400,'Q', curvaNum)
            curvaNum = curvaNum + 1
        '''


    input("Enter to exit")