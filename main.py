from sports.soccer import (get_games_by_date,
                           get_lineups,
                           map_lineups_to_teams,
                           get_total_team_xg,
                           adjust_teams_xg,
                           get_for_and_against_stats,
                           get_goal_data,
                           get_correct_score_odds,
                           get_outcome_odds,
                           print_goal_data,
                           print_correct_score_data,
                           print_outcome_odds,
                           get_goals_over_under_odds,
                           print_over_under_odds)
from util import serialize


games = get_games_by_date("9", "2024-01-14")
teams_lineups = get_lineups()
map_lineups_to_teams(games, teams_lineups)
get_for_and_against_stats(games)
get_total_team_xg(games)
adjust_teams_xg(games)
get_goal_data(games)
get_correct_score_odds(games)
get_outcome_odds(games)
get_goals_over_under_odds(games)


# Get Both teams to score odds

# print_correct_score_data(games)
print_outcome_odds(games)
print_over_under_odds(games)














