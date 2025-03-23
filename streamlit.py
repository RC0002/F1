import base64
import sys
from datetime import datetime
from datetime import time, timedelta
import fastf1
import pytz
from fastf1.ergast import Ergast

import streamlit as st
import pandas as pd
import streamlit as st
import time
import json
import pycountry
import BestLapCompareSpeedAndDeltaBestOfTwoTeam
import Functions
import SimulationFreePracticePaceTeamOrDriversStreamlit
import asyncio
import BestLapCompareTelemetryDeltaBestOfTwoTeamStreamlit
import ChangePositionInRace

sys.setrecursionlimit(2000)  # Set recursion limit to 2000

anno_attuale = datetime.now().year

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        border: none;
        border-color: black;
        /* Rimuovere i bordi dalla tabella */
        table {
            border-collapse: collapse;
            width: 100%;
            border: none;
            border-color: black;
            text-align: left;
        }
        th, td {
            border: 0px solid black;
            padding: 10px;
            text-align: left;
        }
        /* Colore per il passaggio del mouse sulle righe */
        tr:hover {
            background-color: red
        }
    </style>
""", unsafe_allow_html=True)

# Funzioni per le diverse pagine
def pagina_home():
    fuso_orario_locale = pytz.timezone('Europe/Rome')

    col1, col2, col3 = st.columns([2, 1, 1])  # La seconda colonna è più grande


    nextRound = Functions.getEventInformationPerYearAfterSysdate(anno_attuale).iloc[0]
    with col1:
        st.write('Next round:')
        st.title(nextRound["OfficialEventName"])
    with col2:
        # Codice del paese (ad esempio, "us" per Stati Uniti, "it" per Italia)
        paese = pycountry.countries.get(name=nextRound["Country"]).alpha_2.lower()
        # URL per caricare la bandiera direttamente
        bandiera_url = f"https://flagpedia.net/data/flags/h80/{paese}.png"

        # Mostra la bandiera
        st.image(bandiera_url, width=200)


    col1, col3 = st.columns([1, 2])  # La seconda colonna è più grande
    with col1:



        st.write(nextRound['Session1'] +': '+ str(nextRound["Session1Date"].astimezone(fuso_orario_locale)).replace(r'+01:00', ''))
        st.write(nextRound['Session2'] +': '+ str(nextRound["Session2Date"].astimezone(fuso_orario_locale)).replace(r'+01:00', ''))
        st.write(nextRound['Session3'] +': '+ str(nextRound["Session3Date"].astimezone(fuso_orario_locale)).replace(r'+01:00', ''))
        st.write(nextRound['Session4'] +': '+ str(nextRound["Session4Date"].astimezone(fuso_orario_locale)).replace(r'+01:00', ''))
        st.write(nextRound['Session5'] +': '+ str(nextRound["Session5Date"].astimezone(fuso_orario_locale)).replace(r'+01:00', ''))


    with col3:
        nextR = nextRound['Country']
        if nextRound['Country'] == 'Azerbaijan' :
            nextR = "Baku"
        elif nextRound['Country'] == 'United Arab Emirates':
            nextR = "Abu Dhabi"
        elif nextRound['Location'] == 'Imola':
            nextR = "Emilia Romagna"
        elif nextRound['Country'] == 'United Kingdom':
            nextR = "Great Britain"
        elif nextRound['Country'] == 'United States':
            if nextRound['Location'] == 'Miami':
                nextR = 'Miami'
            elif nextRound['Location'] == 'Las Vegas':
                nextR = 'Las Vegas'
            else:
                nextR = 'USA'

        # URL dell'immagine che vuoi visualizzare
        url = 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/'+nextR.replace(" ", "_")+'_Circuit'

        # Mostra l'immagine direttamente in Streamlit
        st.image(url)


    # CountDown
        # Combina la data e l'ora scelte
    scadenza = datetime.combine(nextRound['EventDate'], nextRound['Session5Date'].astimezone(fuso_orario_locale).time())

    # Placeholder per aggiornare il countdown
    countdown_placeholder = st.empty()
    # Loop del countdown
    while True:
        tempo_rimanente = scadenza - datetime.now()

        if tempo_rimanente.total_seconds() <= 0:
            countdown_placeholder.markdown("🎉 Race Time!")
            break

        giorni = tempo_rimanente.days
        ore, resto = divmod(tempo_rimanente.seconds, 3600)
        minuti, secondi = divmod(resto, 60)

        countdown_placeholder.markdown(f"## {giorni} giorni, {ore} ore, {minuti} minuti, {secondi} secondi")
        time.sleep(1)

def pagina_calssifica():

    st.title("CLASSIFICHE MONDIALE F1 " + str(anno_attuale))
    # Crea due colonne
    col1, col2 = st.columns(2)

    with col1:
        ergast = Ergast()
        with st.spinner('Wait for it...'):
            standings = ergast.get_constructor_standings(anno_attuale)
        if (not standings.description.empty):
            st.header("CLASSIFICA COSTRUTTORI " + str(anno_attuale))
            st.markdown(standings.content[0][['position', 'constructorName', 'points', 'wins']].reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)

    with col2:
        ergast = Ergast()
        with st.spinner('Wait for it...'):
            standings = ergast.get_driver_standings(anno_attuale)
        st.header("CLASSIFICA PILOTI " + str(anno_attuale))
        if (not standings.description.empty):
            if (anno_attuale < 2000):
                st.markdown(standings.content[0][['position', 'givenName', 'familyName', 'points','wins','constructorNames']].reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)
            else:
                st.markdown(standings.content[0][['position', 'givenName', 'familyName','driverNumber', 'driverCode', 'points', 'wins', 'constructorNames']].reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)

    if (standings.description.empty):
        Functions.printImageChampNotStarted()

def pagina_calendario():
    st.title("CALENDARIO " + str(anno_attuale))
    ergast = Ergast()
    with st.spinner('Wait for it...'):
        calendario = ergast.get_race_schedule(anno_attuale)
    if (calendario.empty):
        Functions.printImageChampNotStarted()
    else:

        # Rimuovere il tempo "00:00:00" dalle colonne di data (se il tempo è "00:00:00", mostrerò solo la data)
        if(anno_attuale > 2005):
            calendario['raceDate'] = calendario['raceDate'].dt.strftime('%Y-%m-%d')
        if anno_attuale >= 2022:
            calendario['fp1Date'] = calendario['fp1Date'].dt.strftime('%Y-%m-%d')
            calendario['fp2Date'] = calendario['fp2Date'].dt.strftime('%Y-%m-%d')
            calendario['fp3Date'] = calendario['fp3Date'].dt.strftime('%Y-%m-%d')
            calendario['qualifyingDate'] = calendario['qualifyingDate'].dt.strftime('%Y-%m-%d')
            calendario['sprintDate'] = calendario['sprintDate'].dt.strftime('%Y-%m-%d')

        # Rimuovere l'ora "00:00:00" dalle colonne di ora (se il tempo è "00:00:00", mostrerò solo la parte dell'ora)
        if (anno_attuale > 2005):
            # Convertiamo la colonna raceTime in datetime, gestendo il fuso orario
            calendario['raceTime'] = pd.to_datetime(calendario['raceTime'], format='%H:%M:%S%z')
            # Impostiamo il fuso orario UK (Europe/London)
            uk_tz = pytz.timezone('Europe/London')
            # Definiamo il fuso orario locale (ad esempio Europe/Rome)
            fuso_orario_locale = pytz.timezone('Europe/Rome')
            # Calcoliamo la differenza di orario tra UK e il fuso orario locale
            difference = fuso_orario_locale.utcoffset(pd.Timestamp.now()) - uk_tz.utcoffset(pd.Timestamp.now())
            # Estraiamo il numero di ore dalla differenza
            hours_to_add = difference.total_seconds() / 3600
            # Aggiungiamo la differenza in ore agli orari nel fuso orario UK
            calendario['raceTime'] = (calendario['raceTime'] + timedelta(hours=hours_to_add)).dt.time

            calendario['raceTime'] = calendario['raceTime'].apply(lambda x: x if x != '00:00:00' else '')
        if anno_attuale >= 2022:
            calendario['fp1Time'] = pd.to_datetime(calendario['fp1Time'], format='%H:%M:%S%z')
            calendario['fp1Time'] = (calendario['fp1Time'] + timedelta(hours=hours_to_add)).dt.time
            calendario['fp1Time'] = calendario['fp1Time'].apply(lambda x: x if x != '00:00:00' else '')

            calendario['fp2Time'] = pd.to_datetime(calendario['fp2Time'], format='%H:%M:%S%z')
            calendario['fp2Time'] = (calendario['fp2Time'] + timedelta(hours=hours_to_add)).dt.time
            calendario['fp2Time'] = calendario['fp2Time'].apply(lambda x: x if x != '00:00:00' else '')

            calendario['fp3Time'] = pd.to_datetime(calendario['fp3Time'], format='%H:%M:%S%z')
            calendario['fp3Time'] = (calendario['fp3Time'] + timedelta(hours=hours_to_add)).dt.time
            calendario['fp3Time'] = calendario['fp3Time'].apply(lambda x: x if x != '00:00:00' else '')

            calendario['qualifyingTime'] = pd.to_datetime(calendario['qualifyingTime'], format='%H:%M:%S%z')
            calendario['qualifyingTime'] = (calendario['qualifyingTime'] + timedelta(hours=hours_to_add)).dt.time
            calendario['qualifyingTime'] = calendario['qualifyingTime'].apply(lambda x: x if x != '00:00:00' else '')

            calendario['sprintTime'] = pd.to_datetime(calendario['sprintTime'], format='%H:%M:%S%z')
            calendario['sprintTime'] = (calendario['sprintTime'] + timedelta(hours=hours_to_add)).dt.time
            calendario['sprintTime'] = calendario['sprintTime'].apply(lambda x: x if x != '00:00:00' else '')

        # Rimuovere il fuso orario (+00:00) e anche i secondi :00
        if (anno_attuale > 2005):
            calendario['raceTime'] = calendario['raceTime'].astype(str).str.replace(r'\+00:00$', '', regex=True)  # Rimuove il fuso orario
        if anno_attuale >= 2022:
            # Rimuovere il fuso orario (+00:00) e anche i secondi :00
            time_columns = ['fp1Time', 'fp2Time', 'fp3Time', 'qualifyingTime', 'sprintTime']
            for col in time_columns:
                calendario[col] = calendario[col].astype(str).str.replace(r'\+00:00$', '', regex=True)  # Rimuove il fuso orario
                calendario[col] = calendario[col].str.replace(r':00$', '', regex=True)  # Rimuove i :00 alla fine dei secondi
                calendario[col] = calendario[col].astype(str).str.replace(r'NaT$', '', regex=True)
                calendario[col] = calendario[col].str.replace(r'nat$', '', regex=True)

            # Rimuovere il fuso orario (+00:00) e anche i secondi :00
            time_columns = ['sprintDate', 'sprintTime', 'fp3Date' , 'fp3Time']
            for col in time_columns:
                calendario[col] = calendario[col].astype(str).str.replace(r'NaT$', '', regex=True)
                calendario[col] = calendario[col].str.replace(r'nat$', '',regex=True)
        if (anno_attuale < 2005):
            st.markdown(calendario[['round', 'raceName', 'raceDate','circuitName', 'country']].reset_index(drop=True).to_html(index=False),
                        unsafe_allow_html=True)
        elif anno_attuale >= 2022:
            st.markdown(calendario[['round', 'raceName', 'raceDate','raceTime', 'circuitName', 'country', 'fp1Time', 'fp2Time',  'fp3Time', 'qualifyingTime','sprintTime']].reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)
        else:
            st.markdown(calendario[['round', 'raceName', 'raceDate', 'raceTime', 'circuitName', 'country',]].reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)

def pagina_risultati():
    st.title("Risultati")
    #listaCalendario = Functions.getEventNamePerYear(anno_attuale)
    listaCalendario = Functions.getEventNamePerYearBeforeSysdate(anno_attuale)
    col1, col2, col3, col4, col5 = st.columns(5)
    #st.write(fastf1.get_event_schedule(anno_attuale))

    # Posizionare il primo selectbox nella prima colonna
    with col1:
        nameRace = st.selectbox("Scegli la gara", listaCalendario)
    # Posizionare il secondo selectbox nella seconda colonna
    with col2:
        eventi = pd.DataFrame(Functions.getEventPerYear(anno_attuale))
        tipoEvento = eventi.loc[eventi['EventName'] == nameRace, 'EventFormat'].iloc[0]
        roundNumber = eventi.loc[eventi['EventName'] == nameRace, 'RoundNumber'].iloc[0]
        if tipoEvento == "conventional":
            sessionRace = st.selectbox("Scegli la Sessione",
                                       ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'])
            isTest = False
        elif tipoEvento == "sprint_qualifying":
            sessionRace = st.selectbox("Scegli la Sessione",
                                       ['Practice 1', 'Sprint Qualifying', 'Sprint', 'Qualifying', 'Race'])
            isTest = False
        else:
            nameRace = 1
            sessionRace = st.selectbox("Scegli la Sessione", [1, 2, 3])
            isTest = True


    with st.spinner('Wait for it...'):
        st.title(nameRace +' - '+ sessionRace)
        if not isTest:
            session = fastf1.get_session(anno_attuale, nameRace, sessionRace)
        else:
            session = fastf1.get_testing_session(anno_attuale, nameRace, sessionRace)
        session.load()
        ris = session.results[['Position','FullName', 'DriverNumber', 'TeamName']]
        ris['Position'] = (ris['Position'].astype(str).str.replace('\.0', '', regex=True) )
        st.write(ris.reset_index(drop=True).to_html(index=False), unsafe_allow_html=True)

def pagina_impostazioni():
    st.title("Impostazioni")
    eventi_passati = Functions.getEventNamePerYearBeforeSysdate(anno_attuale)
    ultimo_evento = eventi_passati.iloc[0]

    driver_riaperto =Functions.getDriverDefault()

    team_riaperto = Functions.getTeamDefault()

    with st.spinner('Wait for it...'):

        drivers = Functions.getDriverOfTheSession(anno_attuale, ultimo_evento, 'Practice 1')
        teams = Functions.getTeamOfTheSession(anno_attuale, ultimo_evento, 'Practice 1')

        st.write('Selezioni di default')
        driverDefault  = st.multiselect(
            'Scegli Piloti:',
            drivers,
            default=driver_riaperto
        )

        teamDefault = st.multiselect(
            'Scegli Team:',
            teams,
            default=team_riaperto
        )

        with open("driverDefault.json", "w") as json_file:
            json.dump(driverDefault, json_file)

        with open("teamDefault.json", "w") as json_file1:
            json.dump(teamDefault, json_file1)


def pagina_passi_gara():
    st.title("Passo Gara")
    #listaCalendario = Functions.getEventNamePerYear(anno_attuale)
    listaCalendario = Functions.getEventNamePerYearBeforeSysdate(anno_attuale)
    col1, col2, col3, col4, col5 = st.columns(5)
    #st.write(fastf1.get_event_schedule(anno_attuale))

    # Posizionare il primo selectbox nella prima colonna
    with col1:
        nameRace = st.selectbox("Scegli la gara", listaCalendario)
    # Posizionare il secondo selectbox nella seconda colonna
    with col2:
        eventi = pd.DataFrame(Functions.getEventPerYear(anno_attuale))
        tipoEvento = eventi.loc[eventi['EventName'] == nameRace, 'EventFormat'].iloc[0]
        roundNumber = eventi.loc[eventi['EventName'] == nameRace, 'RoundNumber'].iloc[0]
        if tipoEvento == "conventional":
            sessionRace = st.selectbox("Scegli la Sessione", ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'])
            isTest = False
        elif tipoEvento == "sprint_qualifying":
            sessionRace = st.selectbox("Scegli la Sessione", ['Practice 1', 'Sprint Qualifying', 'Sprint', 'Qualifying', 'Race'])
            isTest = False
        else:
            nameRace = 1
            sessionRace = st.selectbox("Scegli la Sessione",[1,2,3])
            isTest = True

    drivers = Functions.getDriverOfTheSession(anno_attuale, nameRace, sessionRace)
    #ergast = Ergast()
    #standing = ergast.get_driver_standings(anno_attuale).content[0]
    #st.write(standing)
    #st.write(standing['constructorNames'] == ['Ferrari'])
    #st.write(standing.loc[standing['constructorNames'] == 'Ferrari', 'driverCode'])

    if(anno_attuale == datetime.now().year):
        d=Functions.getDriverDefault()
    else:
        d = drivers

    pilotiSelezionati = st.multiselect(
        'Piloti',  # Titolo del widget
        options=drivers,  # Lista di opzioni
        default= d  # Valori di default selezionati
    )

    #st.write(pilotiSelezionati, sessionRace, nameRace, tipoEvento)
    #with st.spinner('Wait for it...'):
        #st.pyplot(BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(nameRace, anno_attuale, "Red Bull Racing", "Ferrari", "Mercedes", sessionRace))

    with st.spinner('Wait for it...'):
        SimulationFreePracticePaceTeamOrDriversStreamlit.execute(nameRace, anno_attuale,
                                                                                pilotiSelezionati, sessionRace,
                                                                                '00:00:5.000000',isTest)

def pagina_giro_veloce():
    st.title("Giro Veloce")
    #listaCalendario = Functions.getEventNamePerYear(anno_attuale)
    listaCalendario = Functions.getEventNamePerYearBeforeSysdate(anno_attuale)
    col1, col2, col3, col4, col5 = st.columns(5)
    # st.write(fastf1.get_event_schedule(anno_attuale))

    # Posizionare il primo selectbox nella prima colonna
    with col1:
        nameRace = st.selectbox("Scegli la gara", listaCalendario)
    # Posizionare il secondo selectbox nella seconda colonna
    with col2:
        eventi = pd.DataFrame(Functions.getEventPerYear(anno_attuale))
        tipoEvento = eventi.loc[eventi['EventName'] == nameRace, 'EventFormat'].iloc[0]
        roundNumber = eventi.loc[eventi['EventName'] == nameRace, 'RoundNumber'].iloc[0]
        if tipoEvento == "conventional":
            sessionRace = st.selectbox("Scegli la Sessione",
                                       ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'])
            isTest = False
        elif tipoEvento == "sprint_qualifying":
            sessionRace = st.selectbox("Scegli la Sessione",
                                       ['Practice 1', 'Sprint Qualifying', 'Sprint Race', 'Qualifying', 'Race'])
            isTest = False
        else:
            nameRace = 1
            sessionRace = st.selectbox("Scegli la Sessione", [1, 2, 3])
            isTest = True
    teams = Functions.getTeamOfTheSession(anno_attuale, nameRace, sessionRace)
    teamSelezionati = st.multiselect(
        'Teams',  # Titolo del widget
        options=teams,  # Lista di opzioni
        default= Functions.getTeamDefault()  # Valori di default selezionati
    )

    with st.spinner('Wait for it...'):
        BestLapCompareTelemetryDeltaBestOfTwoTeamStreamlit.execute(nameRace, anno_attuale, teamSelezionati, sessionRace)

def pagina_posizioni_gara():
    st.title("Posizioni in Gara")
    #listaCalendario = Functions.getEventNamePerYear(anno_attuale)
    listaCalendario = Functions.getEventNamePerYearBeforeSysdate(anno_attuale)
    col1, col2, col3, col4, col5 = st.columns(5)
    #st.write(fastf1.get_event_schedule(anno_attuale))

    # Posizionare il primo selectbox nella prima colonna
    with col1:
        nameRace = st.selectbox("Scegli la gara", listaCalendario)
    # Posizionare il secondo selectbox nella seconda colonna
    with col2:
        eventi = pd.DataFrame(Functions.getEventPerYear(anno_attuale))
        tipoEvento = eventi.loc[eventi['EventName'] == nameRace, 'EventFormat'].iloc[0]
        roundNumber = eventi.loc[eventi['EventName'] == nameRace, 'RoundNumber'].iloc[0]
        if tipoEvento == "conventional":
            sessionRace = st.selectbox("Scegli la Sessione", [ 'Race'])
            isTest = False
        elif tipoEvento == "sprint_qualifying":
            sessionRace = st.selectbox("Scegli la Sessione", ['Sprint', 'Race'])
            isTest = False
        else:
            nameRace = 1
            sessionRace = st.selectbox("Scegli la Sessione",[1,2,3])
            isTest = True

    drivers = Functions.getDriverOfTheSession(anno_attuale, nameRace, sessionRace)
    #ergast = Ergast()
    #standing = ergast.get_driver_standings(anno_attuale).content[0]
    #st.write(standing)
    #st.write(standing['constructorNames'] == ['Ferrari'])
    #st.write(standing.loc[standing['constructorNames'] == 'Ferrari', 'driverCode'])

    #---if(anno_attuale == datetime.now().year):
    #---    d=Functions.getDriverDefault()
    #---else:
    #---    d = drivers

    #---pilotiSelezionati = st.multiselect(
        #---    'Piloti',  # Titolo del widget
        #---    options=drivers,  # Lista di opzioni
    #---    default= drivers  # Valori di default selezionati
    #---)

    #st.write(pilotiSelezionati, sessionRace, nameRace, tipoEvento)
    #with st.spinner('Wait for it...'):
        #st.pyplot(BestLapCompareSpeedAndDeltaBestOfTwoTeam.execute(nameRace, anno_attuale, "Red Bull Racing", "Ferrari", "Mercedes", sessionRace))

    with st.spinner('Wait for it...'):
        ChangePositionInRace.execute(nameRace, anno_attuale,drivers, sessionRace,
                                                                                '00:00:5.000000',isTest)



# Menu laterale per la navigazione
st.sidebar.image("logo.png")
#menu = ["Home", "Classifiche", "Calendario", "Info"]
#scelta = st.sidebar.selectbox("Menu", menu)


# Ottieni l'anno corrente
anno_corrente = datetime.now().year
anni_disponibili = list(range(1958, anno_corrente + 1))[::-1]
# Selettore per l'anno, impostando l'anno corrente come valore di default
anno_selezionato = st.sidebar.selectbox("Seleziona un anno:", anni_disponibili, index=0)
anno_attuale = anno_selezionato


# Condizioni per visualizzare il contenuto in base alla selezione
#if scelta == "Home":
#    pagina_home()
#elif scelta == "Classifiche":
#    pagina_calssifica()
#elif scelta == "Calendario":
#    pagina_calendario()
#elif scelta == "Info":
#    pagina_info()

pages = {
    "Menu": [
        st.Page(pagina_home, title="Home", icon=""),
        st.Page(pagina_calssifica, title="Classifiche", icon="🏆"),
        st.Page(pagina_calendario, title="Calendario", icon="🖥️"),
        st.Page(pagina_risultati, title="Risultati", icon="📊"),
        st.Page(pagina_impostazioni, title="Impostazioni", icon="⚙️"),
    ],"Grafici":[
            st.Page(pagina_passi_gara, title="Passo Gara"),
            st.Page(pagina_giro_veloce, title="Giro Veloce"),
            st.Page(pagina_posizioni_gara, title="Posizioni in Gara")]
}

pg = st.navigation(pages)
pg.run()

# Usa l'anno selezionato per modificare altre variabili o eseguire logiche
# Ad esempio, supponiamo che tu voglia fare una chiamata a un'API o a un database che dipenda dall'anno


