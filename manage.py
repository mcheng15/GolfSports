#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://mcheng15:chengcoffey89@sportsmodeldata.cthxyjlr92rk.us-west-2.rds.amazonaws.com:3306/SportsModelDB', debug='False', repository='SportsModelDBRepo')
