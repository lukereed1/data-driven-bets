from scrapers.soccer import get_games_by_date, get_lineups, map_lineups_to_teams, find_teams_stats
from util import serialize
import json


daily_games = get_games_by_date("9", "2023-12-16")
teams_lineups = get_lineups()
games = map_lineups_to_teams(daily_games, teams_lineups)

print(serialize(find_teams_stats(games)))




