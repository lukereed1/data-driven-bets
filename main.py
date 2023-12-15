from scrapers.soccer import find_games_by_date, find_lineups, find_teams_stats
from util import serialize
import json

# daily_games = find_games_by_date(9, "2023-12-16")
teams_lineups = find_lineups()

print(serialize(teams_lineups))


