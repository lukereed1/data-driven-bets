from scrapers.soccer import find_games, find_lineups, find_teams_xg
from util import serialize
import json

daily_games = find_games(9, "2023-12-15")
daily_games = find_lineups(daily_games)


find_teams_xg(daily_games)
