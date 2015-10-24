from BeautifulSoup import BeautifulSoup
import urllib2
import pandas as pd 
import html5lib
import locale 
import LoggerWrapper

locale.setlocale( locale.LC_ALL, 'english_USA' ) 
#use to convert currency string into integers

class Venue: 
    def __init__(self):
        self.venues_list = []

    def addVenue(self, venue):
        self.venues_list.append(venue)

class ESPNTournamentDataScraper: 

    def __init__(self):        
        self.all_tournaments_df = pd.DataFrame()
        self.log = LoggerWrapper.LoggerWrapper()
        self.last_tournament_date = 0

    def ParseAllTournaments(self, num_tournament_ids):   
        self.GetLatestDate()
        for i in xrange(num_tournament_ids):
            print "Starting {0}".format(str(i))
            url= 'http://espn.go.com/golf/leaderboard?tournamentId={0}'.format(str(i))
            print url
            tournament_df = self.ParseSingleTournamentData(url)
            self.all_tournaments_df = self.all_tournaments_df.append(tournament_df)

    def GetLatestDate(self): 
        url= 'http://espn.go.com/golf/leaderboard'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())        
        self.last_tournament_date = soup.findAll(True, {'class': ['date']})[0].contents[0]
        
    def ParseSingleTournamentData(self, url):        
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read());
        emptyDataFrame = pd.DataFrame()
        html_df = pd.DataFrame()

        try: 
            html_df = pd.read_html(url)
        except:
            print "No tables found"
            return emptyDataFrame

        current_date = soup.findAll(True, {'class': ['date']})[0].contents[0]

        if(current_date == self.last_tournament_date):
            self.log.LogWarningMessage("Date is None OR equal to latest tournament")
            return emptyDataFrame           
           
        resultsDf = pd.DataFrame()

        for i in xrange(len(html_df)):
            if(len(html_df[i].columns) > 10):
                resultsDf = html_df[i].dropna(how = 'all')
                break;

        if(len(resultsDf) < 10): 
            self.log.LogWarningMessage("ERROR {0}: Skipped blank tournament".format(i))
            return pd.DataFrame()

        if('EARNINGS' in resultsDf.columns):
            resultsDf.loc[:, 'EARNINGS'] = resultsDf.loc[:,'EARNINGS'].apply(lambda x: locale.atoi(x[1:]))
        resultsDf = resultsDf.drop('CTRY', 1) #drop country column 
        resultsDf = resultsDf.reset_index(drop = True)        
        resultsDf.loc[:, 'DATE'] = current_date     
        
        #grab venues in list format
        html_venues_list  = soup.findAll(True, {'class':['venue']})
        venue_obj = Venue()
        for venue in html_venues_list:
            print venue.contents[0]
            venue_obj.addVenue(venue.contents[0])
        resultsDf.ix[:, 'Venue'] = venue_obj        
                
        #incorrect venue format 
        #if(len(venue_string_array) != 2):
        #    venue_string_array = venue.split('-')
        #    if(len(venue_string_array) != 2):
        #        logging.warning("ERROR {0}: URL {1} has incorrect venue format | IE {2}".format(str(i), url, venue))
        #        continue

        #adding venus 


        #adding course detail 
        #course_detail_array = venue_string_array[1].strip().split(' ')
        #if(len(course_detail_array) == 3):
        #    resultsDf.ix[:, 'Par'] = locale.atoi(course_detail_array[1])
        #    resultsDf.ix[:, 'Yardage'] = locale.atoi(course_detail_array[2])

        competition_level_list = soup.findAll(True, {'class':['key-dates-golf']})

        #no competition level mentioned
        if(len(competition_level_list) == 0):
            self.log.LogWarningMessage("URL {0} : has no key dates section to parse golf level.".format(url))
            return emptyDataFrame

        competition_level = competition_level_list[0].contents[0].contents[0]

        print "Adding Competition Level" 

        #adding competition level 
        if("PGA Tour" in competition_level):
            resultsDf.ix[:, 'Competition Level'] = "PGA"
        elif ("Web.com Tour" in competition_level):
            resultsDf.ix[:, 'Competition Level'] = "Web.com"
        elif ("Euro Tour" in competition_level):
            resultsDf.ix[:, 'Competition Level'] = "Euro"

        resultsDf = resultsDf.replace(to_replace = '-' , value = 0)       

        print "Finished idx {0} ".format(str(i))

        return resultsDf



