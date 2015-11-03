from sqlalchemy import *
from migrate import *

eventsTable = Table("EventsTable", meta, autoload=True)



def upgrade(migrate_engine):
    meta = MetaData(bind = migrate_engine)

    # eventsTable.c.R1.drop()
    # eventsTable.c.R2.drop()
    # eventsTable.c.R3.drop()
    # eventsTable.c.R4.drop()
    eventsTable.c.playerID.drop()
    eventsTable.c.competitionLevelID.drop()
    eventsTable.c.tot.drop()
    eventsTable.c.pos.drop()
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind = migrate_engine)
    eventsTable = Table("EventsTable", meta, autoload=True)

    # r1column = Column("R1", Integer)
    # r2column = Column("R2", Integer)
    # r3column = Column("R3", Integer)
    # r4column = Column("R4", Integer)
    # playerID = Column("playerID", Integer)
    # compColumn = Column("competitionLevelID", Integer)
    # totCol = Column("competitionLevelID", Integer)
    # posCol = Column("competitionLevelID", Integer)
    # r1column.create()
    pass
