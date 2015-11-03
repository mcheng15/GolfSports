import sys
sys.path.append("Utility/")
sys.path.append("Infrastructure/")
sys.path.append("Parser/")

from BeautifulSoup import BeautifulSoup
import pandas as pd
import httplib2
import locale
import logging

from TournamentClasses import Venue
import TournamentColumnConstants
import UtilityFunctions
import TournamentFieldParser
import LoggerWrapper
import LoggingConstants
import WebContentReader

Log = LoggerWrapper.GetLogger(LoggingConstants.GOLF_LOGGER)

locale.setlocale( locale.LC_ALL, 'english_USA' )
#use to convert currency string into integers

Last_Tournament_Date = None

import time

def ParseTournament(idx):
    global Last_Tournament_Date
    if Last_Tournament_Date == None:
        Last_Tournament_Date = GetLatestTournament()
    url= 'http://espn.go.com/golf/leaderboard?tournamentId={0}'.format(str(idx))
    Log.log(logging.DEBUG, "Starting {0}: {1}".format(str(idx), url))
    return ParseSingleTournamentData(url)

def GetLatestTournament():
    url= 'http://espn.go.com/golf/leaderboard'
    soup = BeautifulSoup(GrabWebpageContent(url))
    date = soup.findAll(True, {'class': ['date']})[0].contents[0]
    return date

def FindTournamentDate(soup):
    current_date = soup.findAll(True, {'class': ['date']})[0].contents[0]

    if(current_date == Last_Tournament_Date):
        Log.log(logging.DEBUG, "Date is None OR equal to latest tournament")
        return None
    return current_date

def ParseSingleTournamentData(url):
    #todo only parse to 694
    global Last_Tournament_Date
    soup = BeautifulSoup(WebContentReader.GrabWebpageContent(url))
    emptyDataFrame = pd.DataFrame()
    html_df = pd.DataFrame()

    try:
        html_df = pd.read_html(url)
    except:
        Log.log(logging.DEBUG, "No tournament data found")
        return emptyDataFrame

    resultsDf = pd.DataFrame()

    current_date = FindTournamentDate(soup)

    if(current_date == None):
        return emptyDataFrame

    for i in xrange(len(html_df)):
        if TournamentColumnConstants.PLAYER in html_df[i].columns and TournamentColumnConstants.R1 in html_df[i].columns:
            resultsDf = html_df[i].dropna(how = 'all')
            break;

    if resultsDf.empty:
        Log.log(logging.ERROR, "Tournament has no scores data table")
        return resultsDf

    resultsDf.loc[:, TournamentColumnConstants.DATE] = current_date

    if(len(resultsDf) < 10):
        Log.log(logging.ERROR, "Skipped blank tournament")
        return pd.DataFrame()

    columnsToRemove = ['CTRY', 'EARNINGS', 'FEDEX PTS']
    resultsDf = UtilityFunctions.RemoveColumns(columnsToRemove, resultsDf)

    #grab venues in list format
    htmlVenuesList  = soup.findAll(True, {'class':['venue']})
    venueListObject = TournamentFieldParser.Tournament_ParseVenue((htmlVenuesList))
    resultsDf.ix[:, TournamentColumnConstants.VENUE] = venueListObject

    #find competition level
    competition_level_list = soup.findAll(True, {'class':['tour-logo']})

    [success, data] = TournamentFieldParser.Tournament_ParseCompetition(competition_level_list)
    if(success is False):
        Log.log(logging.ERROR, "{0} Tour logo Section is non existent".format(data))
        return emptyDataFrame

    print "Adding Competition Level"
    resultsDf = TournamentFieldParser.Tournament_AddCompetitionToDF(data, resultsDf, TournamentColumnConstants.COMPLEVEL)

    tourney_name = soup.findAll(True, {'class': ['tourney-name']})
    if(len(tourney_name)>0):
        tourney_name = tourney_name[0].contents[0]
    else:
        tourney_name = "N/A"

    resultsDf.ix[:, TournamentColumnConstants.EVENT] = tourney_name

    #all '-' found in the dataframe representing scores will be replaced with 0
    resultsDf = resultsDf.replace(to_replace = '-' , value = 0)

    #remove all players with nan
    resultsDf = resultsDf[resultsDf[TournamentColumnConstants.PLAYER].apply(str) != 'nan']

    Log.log(logging.DEBUG, "Finished idx {0} ".format(str(i)))

    return resultsDf



