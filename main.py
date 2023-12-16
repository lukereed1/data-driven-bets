from scrapers.soccer import get_games_by_date, get_lineups, map_lineups_to_teams, get_teams_stats
from util import serialize


daily_games = get_games_by_date("9", "2023-12-15")
teams_lineups = get_lineups()
games = map_lineups_to_teams(daily_games, teams_lineups)

print(serialize(get_teams_stats(games)))




