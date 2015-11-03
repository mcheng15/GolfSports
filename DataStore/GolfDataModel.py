import sys
sys.path.append("DataStore/")

from sqlalchemy import Column, ForeignKey, Integer, String, PrimaryKeyConstraint, Date
import DatabaseConnection
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerTable(Base):
    __tablename__ = 'PlayerTable'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String(50), nullable = False, unique = True)

class CompetitionLevel(Base):
    __tablename__ = 'CompetitionLevelTable'
    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String(50), nullable = False, unique = True)

class Course(Base):
    __tablename__ = 'CourseTable'
    __table_args__ = (PrimaryKeyConstraint('name', 'location'),)
    id = Column(Integer, nullable=False, autoincrement=True, unique = True)
    name = Column(String(250), nullable=False)
    location = Column(String(50), nullable=True)
    length = Column(Integer, default=0, nullable=True)

class Event(Base):
    __tablename__ = 'EventTable'
    __table_args__ =  (PrimaryKeyConstraint('name', 'courseID', 'beginDate'),) #player cannot play in same event on different days
    id = Column(Integer, autoincrement=True, unique = True )
    name = Column(String(50), nullable=False)
    courseID = Column(Integer, ForeignKey('CourseTable.id'))
    beginDate = Column(Date, nullable = True)
    endDate = Column(Date, nullable = True)

class ScoresTable(Base):
    __tablename__ = 'ScoreTable'
    id = Column(Integer, autoincrement=True, unique = True)
    __table_args__ =  (PrimaryKeyConstraint('playerID', 'eventID'),)
    playerID = Column(Integer, ForeignKey("PlayerTable.id"))
    eventID = Column(Integer, ForeignKey("EventTable.id"))
    competitionLevelID = Column(Integer, ForeignKey('CompetitionLevelTable.id'))
    R1 = Column(Integer, default = 0)
    R2 = Column(Integer, default = 0)
    R3 = Column(Integer, default = 0)
    R4 = Column(Integer, default = 0)
    R5 = Column(Integer, default = 0)
    total = Column(Integer, default = 0)
    toPar = Column(String(10), default = "")
    pos = Column(String(10), default = "0")

class StatsModel(Base):
    __tablename__ = 'StatsTable'
    id = Column(Integer, autoincrement=True, unique = True)
    __table_args__ = (PrimaryKeyConstraint('playerId', 'compLevelId', 'roundsPlayed', 'year', 'masterStat', 'minorStat'),)
    playerId = Column(Integer, ForeignKey("PlayerTable.id"))
    compLevelId = Column(Integer, ForeignKey("CompetitionLevelTable.id"))
    year = Column(Integer, nullable = False, autoincrement=False)
    roundsPlayed = Column(Integer, default = 0)
    masterStat = Column(String(10), default = "")
    minorStat = Column(String(10), default = "")
    statValue = Column(String(10), default = "")

SportsModelSession = DatabaseConnection.CreateSportModelDBEngineSession(Base)

# sportsModelSession.add_all(
#     [CompetitionLevel(name = "PGA Tour"),
#      CompetitionLevel(name = "Web.com Tour"),
#      CompetitionLevel(name = "Euro Tour")]
# )
# sportsModelSession.commit()