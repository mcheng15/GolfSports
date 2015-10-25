import sys
sys.path.append("Infrastructure/")

from TournamentClasses import Venue

def Tournament_ParseDate(strDate):
    return

def Tournament_ParseVenue(htmlVenueList):
    venue_obj = Venue()
    for venue in htmlVenueList:
        print venue.contents[0]
        venue_obj.addVenue(venue.contents[0])

    return venue_obj

#returns success or fail, then data
def Tournament_ParseCompetition(htmlCompetitionList):
    if(len(htmlCompetitionList) != 1):
        return [False, len(htmlCompetitionList)]
    return [True, htmlCompetitionList[0]['alt']]

def Tournament_AddCompetitionToDF(competitionName, df):
    #adding competition level
    if("PGA Tour" in competitionName):
        df.ix[:, 'Competition Level'] = "PGA"
    elif ("Web.com Tour" in competitionName):
        df.ix[:, 'Competition Level'] = "Web.com"
    elif ("Euro Tour" in competitionName):
        df.ix[:, 'Competition Level'] = "Euro"
    return df

