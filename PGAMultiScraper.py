from PGATourStatsScraper import PGATourStatsScraper as PGAScraper
import pandas as pd

class PGAMultiScraper(object):
    """Scrapes multiple stats. Return dict of players and dataframes of stats"""

    def __init__(self): 
        self.player_stats_dict = {}

    """
    Collect stats from pga site
    stat_list: list of tuples [stat_id, stat_name] e.g. [ (448, 'Stat1'), (447, 'Stat2') ]    
    """
    def CollectStats(self, stat_list, from_year, to_year):
        for stat_id, stat_name in stat_list:
            pga_scraper = PGAScraper(stat_id, stat_name)
            pga_scraper.ParseStatForAllYears(from_year, to_year)   
            self.__AddStatToDictionary(pga_scraper)        
            
   
    """
    Combines stats to player stats dictionary. Just adds to the dataframe associated with that player
    """
    def __AddStatToDictionary(self, pga_scraper):
        pga_dict = pga_scraper.CreatePlayerDictionary()                                                                            
        for player_name in pga_dict.keys():
            if(player_name not in self.player_stats_dict.keys()): #player is new
                self.player_stats_dict[player_name] = pga_dict[player_name]
            else: #player is not new, take the concat                 
                self.player_stats_dict[player_name] = pd.concat([self.player_stats_dict[player_name], pga_dict[player_name]], axis = 1, ignore_index = False, join = 'outer') 




