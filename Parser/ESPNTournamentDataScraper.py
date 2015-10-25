import sys
sys.path.append("Utility/")
sys.path.append("Infrastructure/")
sys.path.append("Parser/")
from TournamentClasses import Venue
import UtilityFunctions
import TournamentFieldParser
import urllib2
import locale

from BeautifulSoup import BeautifulSoup
import pandas as pd

import LoggerWrapper

locale.setlocale( locale.LC_ALL, 'english_USA' )
#use to convert currency string into integers

all_tournaments_df = pd.DataFrame()
log = LoggerWrapper.LoggerWrapper()
last_tournament_date = 0

def ParseAllTournaments(self, last_tournament_id_to_parse):
    last_tournament_date = GetLatestTournament()
    for i in xrange(last_tournament_id_to_parse):
        print "Starting {0}".format(str(i))
        url= 'http://espn.go.com/golf/leaderboard?tournamentId={0}'.format(str(i))
        print url
        tournament_df = ParseSingleTournamentData(url)
        all_tournaments_df = all_tournaments_df.append(tournament_df)

def GetLatestTournament():
    url= 'http://espn.go.com/golf/leaderboard'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    date = soup.findAll(True, {'class': ['date']})[0].contents[0]
    return date

def ParseSingleTournamentData(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    emptyDataFrame = pd.DataFrame()
    html_df = pd.DataFrame()

    try:
        html_df = pd.read_html(url)
    except:
        print "No tables found"
        return emptyDataFrame

    resultsDf = pd.DataFrame()

    current_date = soup.findAll(True, {'class': ['date']})[0].contents[0]

    if(current_date == last_tournament_date):
        log.LogWarningMessage("Date is None OR equal to latest tournament")
        return emptyDataFrame

    for i in xrange(len(html_df)):
        if(len(html_df[i].columns) > 10):
            resultsDf = html_df[i].dropna(how = 'all')
            break;

    resultsDf.loc[:, 'DATE'] = current_date

    if(len(resultsDf) < 10):
        log.LogWarningMessage("ERROR {0}: Skipped blank tournament".format(i))
        return pd.DataFrame()

    columnsToRemove = ['CTRY', 'EARNINGS', 'FEDEX PTS', 'POS']
    resultsDf = UtilityFunctions.RemoveColumns(columnsToRemove, resultsDf)

    #grab venues in list format
    htmlVenuesList  = soup.findAll(True, {'class':['venue']})
    venueListObject = TournamentFieldParser.Tournament_ParseVenue((htmlVenuesList))
    resultsDf.ix[:, 'Venue'] = venueListObject

    #adding course detail
    #course_detail_array = venue_string_array[1].strip().split(' ')
    #if(len(course_detail_array) == 3):
    #    resultsDf.ix[:, 'Par'] = locale.atoi(course_detail_array[1])
    #    resultsDf.ix[:, 'Yardage'] = locale.atoi(course_detail_array[2])

    #find competition level
    competition_level_list = soup.findAll(True, {'class':['tour-logo']})

    [success, data] = TournamentFieldParser.Tournament_ParseCompetition(competition_level_list)
    if(success is False):
        log.LogWarningMessage("URL {0} : has {1} tour logo section.".format(url, data))
        return emptyDataFrame

    print "Adding Competition Level"
    resultsDf = TournamentFieldParser.Tournament_AddCompetitionToDF(data, resultsDf)

    #all '-' found in the dataframe representing scores will be replaced with 0
    resultsDf = resultsDf.replace(to_replace = '-' , value = 0)

    print "Finished idx {0} ".format(str(i))

    return resultsDf



