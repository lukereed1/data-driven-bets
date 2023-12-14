from scrapers.soccer import find_games, find_lineups
from util import get_team_stats_url
import json

daily_games = find_games(9, "2023-12-15")
daily_games = find_lineups(daily_games)


print(get_team_stats_url("Nott'ham Forest"))

# print(json.dumps(daily_games, indent=2, default=lambda obj: obj.__dict__))