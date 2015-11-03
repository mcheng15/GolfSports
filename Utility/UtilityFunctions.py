import re
from datetime import datetime

def RemoveColumns(columnsToRemove, resultsDf):
    columnsToRemove = set(resultsDf.columns).intersection(set(columnsToRemove))
    resultsDf = resultsDf.drop(columnsToRemove, 1) #drop and earnings country column
    resultsDf = resultsDf.reset_index(drop = True)
    return resultsDf

def GetColumnValuesInRow(col, row):
    return row[col] if col in row.keys() else None

def GetUniqueValuesInColumn(df, columnName):
    if(columnName in df.columns):
        return df[columnName].unique()
    return []

#the goal of the strip is to enforce structure and identify circumstances when this is not correct

def StripDateIntoDateList(date): #format January 1-4, 2011
    match = re.match(r'(\w+) (\d+)-(\d+), (\d+)', date)
    if match == None:
        return []
    datesList = []

    dateSplit = filter(None, match.groups())
    datesList.append(datetime.strptime("{0} {1} {2}".format(dateSplit[0], dateSplit[1], dateSplit[3]),
                                       "%B %d %Y"))
    datesList.append(datetime.strptime("{0} {1} {2}".format(dateSplit[0], dateSplit[2], dateSplit[3]),
                                           "%B %d %Y"))
    return datesList

def StripMultipleMonthDateList(date):
    match = re.match(r'(\w+) (\d+) to (\w+) (\d+), (\d+$)', date.strip())
    if match == None:
        return []
    dateSplit = filter(None, match.groups())
    datesList = []
    datesList.append(datetime.strptime("{0} {1} {2}".format(dateSplit[0], dateSplit[1], dateSplit[4]),
                                       "%B %d %Y"))
    datesList.append(datetime.strptime("{0} {1} {2}".format(dateSplit[2], dateSplit[3], dateSplit[4]),
                                       "%B %d %Y"))
    return datesList