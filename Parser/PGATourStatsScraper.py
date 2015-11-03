from BeautifulSoup import BeautifulSoup
import pandas as pd
import sys
import re

sys.path.append("Infrastructure/")
import LoggerWrapper
import WebContentReader
import StatColumnConstants
import logging

Log = LoggerWrapper.GetLogger(LoggingConstants.GOLF_STATS_LOGGER)

def FindStatName(soup, statId, year):
    tagList = soup.findAll(True, { 'name': 'title'})
    if(len(tagList) != 1):
        Log.log("ERROR {0}|{1}: Multiple Stat names found.".format(statId, year))
        return None

    if('content' not in tagList[0].attrMap.keys()):
        Log.log("ERROR {0}|{1}: Master Stat name not found.".format(statId, year))
        return None

    match = re.match('^.+;(.*$)', tagList[0]['content'])

    if(match.groups() == None):
        Log.log("ERROR {0}|{1}: Master Stat name does not exist".format(statId, year))
        return None

    return match.groups()[0].strip()


def ParseStatForYear(statId, year, competitionName):
    url = 'http://www.pgatour.com/stats/stat.{0}.{1}.html'.format(statId, year)

    soup = BeautifulSoup(WebContentReader.GrabWebpageContent(url));

    masterStatName = FindStatName(soup, statId, year)

    emptyDataFrame = pd.DataFrame()
    html_df = pd.DataFrame()

    try:
        html_df = pd.read_html(url)
    except:
        print "No tables found"
        return emptyDataFrame

    if(len(html_df) == 0):
        Log.log(logging.ERROR, "ERROR - {0}|{1}: Skipping blank html file".format(statId, year))
        return emptyDataFrame

    #find column names using thead (which is the header of the table)
    columns_tag = soup.findAll('thead')
    if(len(columns_tag) > 1):
        Log.log(logging.ERROR, "Multiple Theads found")
        return emptyDataFrame

    column_names = [x.contents[0].strip() if len(x.contents) > 0 else '' for x in columns_tag[0].findAll('td') ]

    single_year_stats_df = html_df[-1]
    if(len(single_year_stats_df.columns) != len(column_names)):
        Log.log(logging.ERROR, "ERROR - {0}|{1}: Column names mismatch between pandas and html".format(statId, year))
        return emptyDataFrame

    single_year_stats_df.columns = column_names
    single_year_stats_df[StatColumnConstants.PLAYER] = [x.replace(u'\xa0', u' ') for x in single_year_stats_df[StatColumnConstants.PLAYER]]
    single_year_stats_df.ix[:, StatColumnConstants.YEAR] = year
    single_year_stats_df.ix[:, StatColumnConstants.MASTERSTAT]= masterStatName
    single_year_stats_df.ix[:, StatColumnConstants.COMPETITION] = competitionName
    single_year_stats_df.dropna(how = 'all', inplace=True)
    return single_year_stats_df