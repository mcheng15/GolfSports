import sys
sys.path.append("Parser/")
sys.path.append("")
import ESPNTournamentDataScraper
from PGAMultiScraper import PGAMultiScraper as PGAMS

data_scraper = ESPNScraper()
data_scraper.ParseAllTournaments(10)

list = [(448, 'Stat1'), (447, 'Stat2')]
scrape = PGAMS()
scrape.CollectStats(list, 2010, 2016)
