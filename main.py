from scrapers.soccer import find_games, find_lineups, find_teams_stats
from util import serialize
import json

daily_games = find_games(9, "2023-12-15")
daily_games = find_lineups(daily_games)


print(serialize(find_teams_stats(daily_games)))
