import urllib2

from BeautifulSoup import BeautifulSoup
import pandas as pd

import LoggerWrapper


class PGATourStatsScraper:
    """Scrape stats from PGATour for all years"""

    def __init__(self, stat_id, stat_name): 
        self.all_stats_df = pd.DataFrame()
        self.log = LoggerWrapper.LoggerWrapper()
        self.stat_id = stat_id
        self.stat_name = stat_name;
        self.__PLAYER_NAME = '{0}_PLAYER NAME'.format(stat_name)

    def ParseStatForAllYears(self, from_year, to_year):
        for year in range(from_year, to_year):   
            url = 'http://www.pgatour.com/stats/stat.{0}.{1}.html'.format(self.stat_id, year)
            print "{0} - {1}".format(year, url)
            self.log.LogWarningMessage("{0} - {1}".format(year, url))

            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read());
            emptyDataFrame = pd.DataFrame()
            html_df = pd.DataFrame()

            try: 
                html_df = pd.read_html(url)
            except:
                print "No tables found"
                return emptyDataFrame

            if(len(html_df) == 0):
                self.log.LogWarningMessage("Skipping blank html file")
                continue;

            #find column names using thead (which is the header of the table)
            columns_tag = soup.findAll('thead')
            if(len(columns_tag) > 1):
                self.log.LogWarningMessage("Multiple Theads found")
                continue;

            column_names = ["{0}_{1}".format(self.stat_name, x.contents[0]) if len(x.contents) > 0 else '' for x in columns_tag[0].findAll('td') ]                       

            single_year_stats_df = html_df[1]
            if(len(single_year_stats_df.columns) != len(column_names)):
                self.log.LogWarningMessage("Column names mismatch")
                continue

            single_year_stats_df.columns = column_names
            single_year_stats_df[self.__PLAYER_NAME] = [x.replace(u'\xa0', u' ') for x in single_year_stats_df[self.__PLAYER_NAME]]
            single_year_stats_df.ix[:, 'Year'] = year
            self.all_stats_df = self.all_stats_df.append(single_year_stats_df)
        self.all_stats_df = self.all_stats_df.dropna(how = 'all', axis = 1)

    def CreatePlayerDictionary(self):
        player_stat_dict = {}

        if(self.__PLAYER_NAME not in self.all_stats_df.columns):
            print 'Could not Create Player Dictionary. PLAYER NAME column does not exist'

        for player_name in self.all_stats_df[self.__PLAYER_NAME].unique():
            player_stat_dict[player_name] = self.all_stats_df[self.all_stats_df[self.__PLAYER_NAME] == player_name].set_index(keys = 'Year', drop = 'True')

        return player_stat_dict    