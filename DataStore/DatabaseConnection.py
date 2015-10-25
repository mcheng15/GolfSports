from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None

def CreateSportModelDBEngineSession(SportsModelDBBase):
    engine = create_engine('mysql://mcheng15:chengcoffey89@sportsmodeldata.cthxyjlr92rk.us-west-2.rds.amazonaws.com:3306/SportsModelDB')
    SportsModelDBBase.metadata.bind = engine
    SportsModelDBBase.metadata.create_all()
    Session = sessionmaker(bind = engine)
    return Session()



