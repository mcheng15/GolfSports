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
    __tablename__ = 'EventsTable'
    __table_args__ =  (PrimaryKeyConstraint('playerID', 'beginDate'),) #player cannot play in same event on different days
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, autoincrement=True, unique = True)
    name = Column(String(50), nullable=False)
    playerID = Column(Integer, ForeignKey("PlayerTable.id"))
    courseID = Column(Integer, ForeignKey('CourseTable.id'))
    competitionLevelID = Column(Integer, ForeignKey('CompetitionLevelTable.id'))
    R1 = Column(Integer, default = 0)
    R2 = Column(Integer, default = 0)
    R3 = Column(Integer, default = 0)
    R4 = Column(Integer, default = 0)
    tot = Column(Integer, default = 0)
    pos = Column(Integer, default = 0)
    beginDate = Column(Date, nullable = False)
    endDate = Column(Date, nullable = True)

sportsModelSession = DatabaseConnection.CreateSportModelDBEngineSession(Base)

# sportsModelSession.add_all(
#     [CompetitionLevel(name = "PGA Tour"),
#      CompetitionLevel(name = "Web.com Tour"),
#      CompetitionLevel(name = "Euro Tour")]
# )
# sportsModelSession.commit()