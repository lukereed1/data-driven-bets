from scrapers.soccer import find_games_by_date, find_lineups, map_lineups_to_teams
from util import serialize
import json


daily_games = find_games_by_date("9", "2023-12-16")
teams_lineups = find_lineups()
games = map_lineups_to_teams(daily_games, teams_lineups)

print(serialize(games))




