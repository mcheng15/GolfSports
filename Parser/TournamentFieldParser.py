import sys
sys.path.append("Infrastructure/")

from TournamentClasses import Venue

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

def Tournament_AddCompetitionToDF(competitionName, df, competitionColumnName):
    #adding competition level
    if("PGA Tour" in competitionName):
        df.ix[:, competitionColumnName] = "PGA"
    elif ("Web.com Tour" in competitionName):
        df.ix[:, competitionColumnName] = "Web.com"
    elif ("European Tour" in competitionName):
        df.ix[:, competitionColumnName] = "Euro"
    return df

