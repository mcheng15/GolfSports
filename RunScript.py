from ESPNTournamentDataScraper import ESPNTournamentDataScraper as ESPNScraper
from PGAMultiScraper import PGAMultiScraper as PGAMS
import pandas as pd 

data_scraper = ESPNScraper()
data_scraper.ParseAllTournaments(2500)

list = [(448, 'Stat1'), (447, 'Stat2')]
scrape = PGAMS()
scrape.CollectStats(list, 2010, 2016)
