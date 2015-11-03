from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None

# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
# #Python2
# class MyClass(BaseClass):
#     __metaclass__ = Singleton


def CreateSportModelDBEngineSession(SportsModelDBBase):
    engine = create_engine('mysql://mcheng15:chengcoffey89@sportsmodeldata.cthxyjlr92rk.us-west-2.rds.amazonaws.com:3306/SportsModelDB')
    SportsModelDBBase.metadata.bind = engine
    SportsModelDBBase.metadata.create_all()
    Session = sessionmaker(bind = engine)
    return Session()



