from sports.soccer import (get_games_by_date,
                           get_lineups,
                           map_lineups_to_teams,
                           get_total_team_xg,
                           adjust_teams_xg,
                           get_for_and_against_stats,
                           get_goal_data,
                           get_correct_score_odds,
                           print_goal_data)
from util import serialize


games = get_games_by_date("9", "2023-12-21")
teams_lineups = get_lineups()
map_lineups_to_teams(games, teams_lineups)
get_for_and_against_stats(games)
get_total_team_xg(games)
adjust_teams_xg(games)
get_goal_data(games)
get_correct_score_odds(games)
print(serialize(games))












