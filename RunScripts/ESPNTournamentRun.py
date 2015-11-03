import LoggerWrapper
import sys
sys.path.append("Parser/")
sys.path.append("Infrastructure/")
sys.path.append("DatabaseWriter")
import LoggingConstants
import ESPNTournamentDataScraper
import TournamentWriter
import logging

LoggerWrapper.InitializeLogger(LoggingConstants.GOLF_LOGGER, LoggingConstants.GOLF_LOG_FILE_NAME)
Log = LoggerWrapper.GetLogger(LoggingConstants.GOLF_LOGGER)
total_tournaments = 0

for idx in xrange(2700, 3000):
    tournament_df = ESPNTournamentDataScraper.ParseTournament(idx)
    if(len(tournament_df) > 0):
        total_tournaments+=1
    TournamentWriter.WriteTournamentDFToDatabase(tournament_df, idx)
    Log.log(logging.DEBUG, "COMPLETE WRITE OF {0}".format(idx))

LoggerWrapper.FileHandler.close()

