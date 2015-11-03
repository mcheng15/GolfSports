import sys
sys.path.append("DataStore/")
sys.path.append("Infrastructure/")
sys.path.append("Utility/")
import logging

from GolfDataModel import PlayerTable as Player
from GolfDataModel import CompetitionLevel as CompetitionLevel
from GolfDataModel import Course as CourseTable
from GolfDataModel import Event as Event
from GolfDataModel import ScoresTable as Score
from GolfDataModel import StatsModel as Stats

from TournamentClasses import Course
import TournamentColumnConstants
import LoggingConstants
import StatColumnConstants

import UtilityFunctions
import LoggerWrapper

Log = LoggerWrapper.GetLogger(LoggingConstants.GOLF_LOGGER)

def AddStatToTable(row, masterStat, compLevel, SportsSession):
    playerQuery = SportsSession.query(Stats).join(Player).filter(
        Stats.playerId == Player.id).filter(Player.name == row[StatColumnConstants.PLAYER])

    if playerQuery.count() == 0:
        Log.log(logging.ERROR, "Player {0} does not exist".format(row[StatColumnConstants.PLAYER]))
        return

    playerId = playerQuery.all()[0].id

    compQuery= SportsSession.query(Stats).join(CompetitionLevel).filter(
        Stats.compLevelId == CompetitionLevel.id).filter(CompetitionLevel.name == compLevel)

    if compQuery.count() == 0:
        Log.log(logging.ERROR, "Competition {0} does not exist".format(row[StatColumnConstants.PLAYER]))
        return

    compId = compQuery.all()[0].id

    nonStatRows = [StatColumnConstants.PLAYER, StatColumnConstants.ROUNDSPLAYED]
    detailedStatsColumns = set(row.keys()) - set(nonStatRows)

    for statName in detailedStatsColumns:
        statQuery = SportsSession.query(Stats).filter(Stats.compLevelId == compId, Stats.masterStat == masterStat,
                                                      Stats.minorStat == statName, Stats.playerId == playerId,
                                                      Stats.roundsPlayed == row[StatColumnConstants.ROUNDSPLAYED],
                                                      Stats.year == row[StatColumnConstants.YEAR])
        if statQuery.count() == 0:
            Log.log(logging.WARNING, "Master Stat {0}  | Minor Stat {1} already exists".format(masterStat, statName))
            continue

        SportsSession.add(Stats(playerId = playerId, compLevelId = compId,
                                year = row[StatColumnConstants.YEAR],
                                roundsPlayed = row[StatColumnConstants.ROUNDSPLAYED],
                                masterStat = masterStat,
                                minorStat = statName,
                                statValue = row[statName]))

def AddPlayer(playerName, SportsSession):
    global Log
    playerCount = SportsSession.query(Player).filter(Player.name == playerName).count()
    if(playerCount == 0):
        Log.log(logging.DEBUG, "Added player {0} to database".format(playerName))
        SportsSession.add(Player(name = playerName))
    else:
         Log.log(logging.DEBUG, "Player {0} NOT added to database".format(playerName))

def AddCompetitionLevel(competitionLevel, SportsSession):
    global Log
    queryCount = SportsSession.query(CompetitionLevel).filter(CompetitionLevel.name == competitionLevel).count()
    if(queryCount == 0):
        Log.log(logging.DEBUG, "Added competition {0} to database".format(competitionLevel))
        SportsSession.add(CompetitionLevel(name = competitionLevel))
    else:
        Log.log(logging.DEBUG, "Competition {0} not added to database".format(competitionLevel))

def AddCourse(courseObj, SportsSession):
    global Log
    queryCount = SportsSession.query(CourseTable).filter(CourseTable.name == courseObj.name, CourseTable.location == courseObj.location).count()
    if(queryCount == 0):
        Log.log(logging.DEBUG, "Added Course {0} to database".format(courseObj.name))
        SportsSession.add(CourseTable(name = courseObj.name, location = courseObj.location, length = courseObj.length))
    else:
        Log.log(logging.DEBUG, "Course {0} not added to database".format(courseObj.name))

def AddEvent(eventName, datesList, courseList, SportsSession):
    global Log
    if len(datesList) > 2 | len(datesList) == 0 | len(courseList) == 0:
        Log.log(logging.ERROR, "Nothing added for {0} due to no date / course list".format(eventName))
        return

    beginDate = datesList[0]
    endDate = None
    if len(datesList) == 2:
        endDate = datesList[1]

    for course in courseList: #iterate through all courses
        courseQuery = SportsSession.query(CourseTable).filter(CourseTable.name == course.name, CourseTable.location == course.location)
        for row in courseQuery: #iterate through all stored courses (should only return one result since name and location is unique combination)
            eventQuery = SportsSession.query(Event).filter(Event.name == eventName, Event.beginDate == beginDate, Event.courseID == row.id).count()
            if eventQuery  > 0: #event exists that matches name, date, and courseid
                Log.log(logging.WARNING, "Event {0} already exists".format(eventName))
                continue
            Log.log(logging.DEBUG, "Added Event {0}".format(eventName))
            SportsSession.add(Event(name = eventName, beginDate=beginDate, endDate=endDate, courseID = row.id))

def GetEventCompetitionId(competitionLevel, eventName, date, courseList, SportsSession):
    global Log
    if(len(date) == 0 | len(courseList) == 0):
        Log.log(logging.ERROR, "Could not add scores in event {0}".format(eventName))
        return []

    compQuery = SportsSession.query(CompetitionLevel).filter(CompetitionLevel.name == competitionLevel)
    if compQuery.count() == 0:
        Log.log(logging.ERROR, "Could not find competition for {0} in event {1}".format(competitionLevel, eventName))
        return []

    compId = compQuery.all()[0].id

    courseQuery = SportsSession.query(CourseTable).filter(CourseTable.name == courseList[0].name, CourseTable.location == courseList[0].location)
    if courseQuery.count() == 0:
        Log.log(logging.ERROR, "Could not find course for {0} in event {1}".format(courseList[0].name, eventName))
        return []

    courseId = courseQuery.all()[0].id

    eventQuery = SportsSession.query(Event).filter(Event.name == eventName, Event.beginDate == date[0], Event.courseID == courseId)
    if eventQuery.count() == 0:
        Log.log(logging.ERROR, "Could not find event {0} for beginDate {1} and courseId {2}".format(eventName, date[0], courseId))
        return []

    eventId = eventQuery.all()[0].id

    return [compId, eventId]

def AddScoreToTable(row, compId, eventId, SportsSession):
    global Log
    playerName = row[TournamentColumnConstants.PLAYER]

    playerQuery = SportsSession.query(Player).filter(Player.name == playerName)
    if playerQuery.count() == 0:
        Log.log(logging.DEBUG, "Adding score: Player {0} does not exist in table".format(playerName))
        return

    playerId = playerQuery.all()[0].id

    scoreQuery = SportsSession.query(Score).filter(Score.playerID == playerId, Score.eventID == eventId, Score.competitionLevelID == compId).count()
    if(scoreQuery > 0):
        Log.log(logging.DEBUG, "Adding score: Score already exists for playerId {0} eventId {1} and competitionLevel {2}".format(playerId, eventId, compId))
        return

    SportsSession.add(Score(playerID = playerId, eventID = eventId, competitionLevelID = compId,\
                            R1 = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.R1, row),\
                            R2 = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.R2, row),\
                            R3 = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.R3, row),\
                            R4 = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.R4, row),\
                            R5 = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.R5, row),\
                            total = UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.TOTAL, row),\
                            toPar = str(UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.TOPAR, row)),\
                            pos = str(UtilityFunctions.GetColumnValuesInRow(TournamentColumnConstants.POS, row))))\

    print "SportsSession has successfully added scores {0}".format(playerName)
    return None



