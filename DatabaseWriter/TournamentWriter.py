import sys
sys.path.append("DataStore/")
sys.path.append("DatabaseWriter/")
sys.path.append("Infrastructure/")
sys.path.append("Parser/")
sys.path.append("Utility/")

from TournamentClasses import Venue, Course
import TournamentClasses
import TournamentColumnConstants
import UtilityFunctions
import pandas as pd
import GolfDataOperations
import GolfDataModel
import pandas as pd

import logging
import LoggerWrapper
import LoggingConstants

Log = LoggerWrapper.GetLogger(LoggingConstants.GOLF_LOGGER)

#only write
def WriteTournamentDFToDatabase(all_tournaments_df, idx):
    global Log
    Log.log(logging.DEBUG, "Start writing to database")
    #write competition level
    if(len(all_tournaments_df) == 0):
        Log.log(logging.ERROR, "Error {0}: Tournament length is 0".format(idx))
        return

    uniqueCompLevel = UtilityFunctions.GetUniqueValuesInColumn(all_tournaments_df, TournamentColumnConstants.COMPLEVEL)

    if len(uniqueCompLevel) == 0:
        Log.log(logging.ERROR, "Error {0}: No competition level specified".format(idx))
        return

    for compLevel in uniqueCompLevel:
        GolfDataOperations.AddCompetitionLevel(compLevel, GolfDataModel.SportsModelSession)
    GolfDataModel.SportsModelSession.commit()

    #writing players
    uniquePlayers = UtilityFunctions.GetUniqueValuesInColumn(all_tournaments_df, TournamentColumnConstants.PLAYER)

    if len(uniquePlayers) == 0:
        Log.log(logging.DEBUG, "Error {i}: No PLAYERS specified".format(idx))
        return

    for player in uniquePlayers:
        GolfDataOperations.AddPlayer(player, GolfDataModel.SportsModelSession)

    GolfDataModel.SportsModelSession.commit()
    #writing courses
    courseList = []
    uniqueVenues = all_tournaments_df[TournamentColumnConstants.VENUE].unique()

    if len(uniqueVenues) == 0:
        Log.log(logging.DEBUG, "Error: No VENUES specified")
        return

    for venueObj in uniqueVenues:
        if len(venueObj.venues_list) == 0:
            Log.log(logging.ERROR, "ERROR {0}: Skipped tournnament. Does not have any venues...".format(idx))
            return
        for venue in venueObj.venues_list:
            courseObj = TournamentClasses.ConvertVenueToCourseClass(venue)
            courseList.append(courseObj)
            GolfDataOperations.AddCourse(courseObj, GolfDataModel.SportsModelSession)
    GolfDataModel.SportsModelSession.commit()

    #writing the events
    eventName = all_tournaments_df[TournamentColumnConstants.EVENT].iloc[0] #one event per dataframe
    date = all_tournaments_df[TournamentColumnConstants.DATE].iloc[0] #one date per dateframe

    convertedDateTimeList = UtilityFunctions.StripDateIntoDateList(date) #intra date list
    if(len(convertedDateTimeList) == 0):
        convertedDateTimeList = UtilityFunctions.StripMultipleMonthDateList(date) #multiple month list

    #todo: handle multiple year case
    if len(convertedDateTimeList) == 0:
        Log.log(logging.ERROR, "Error {0} Date format is INCORRECT PLEASE CHECK".format(idx))


    GolfDataOperations.AddEvent(eventName, convertedDateTimeList, courseList, GolfDataModel.SportsModelSession)
    GolfDataModel.SportsModelSession.commit()

    #writing the actual score
    idList = GolfDataOperations.GetEventCompetitionId(uniqueCompLevel[0], eventName, convertedDateTimeList, courseList, GolfDataModel.SportsModelSession)

    if len(idList) == 0:
        Log.log(logging.DEBUG, "ERROR {0}: IDS do not exist for competition and event".format(idx))
        return

    all_tournaments_df.apply(lambda x: GolfDataOperations.AddScoreToTable(x, idList[0], idList[1], GolfDataModel.SportsModelSession), axis = 1)

    Log.log(logging.DEBUG, "Complete writing to database")

    GolfDataModel.SportsModelSession.commit()




