from util import team_name_map, get_soup, team_stats_page, three_letter_abbreviation
from models.soccer.game import Game
from models.soccer.team import Team
from models.soccer.goal_chance import GoalChance
from models.soccer.correct_score import CorrectScore
from models.soccer.over_under import OverUnder
from unidecode import unidecode
import math
import pandas as pd
from tabulate import tabulate


def get_games_by_date(league_id, date):
    url = f"https://fbref.com/en/matches/{date}"
    soup = get_soup(url)
    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")
    games = []

    if league_games:
        for game in league_games:
            home = game.find("td", {"data-stat": "home_team"})
            away = game.find("td", {"data-stat": "away_team"})
            time = game.find("td", {"data-stat": "start_time"})

            if home and away:
                home_team = home.find("a").get_text()
                away_team = away.find("a").get_text()
                try:
                    start_time = time.find("span", {"class": "venuetime"}).get_text()
                except Exception as e:
                    start_time = "Not shown"
                    print(f"No start time displayed: {e}")

                game = Game(home_team, away_team, date, start_time)
                games.append(game)

    return games


def get_lineups():
    url = "https://www.fantasyfootballscout.co.uk/team-news/"
    soup = get_soup(url)
    teams_info = soup.find("ol", {"class": "news"}).find_all("li", recursive=False)
    all_team_lineups = []

    for team in teams_info:
        team_name = team.find("div", {"class": "story-wrap"}).find("h2").get_text()
        team_lineup_element = team.find("div", {"class": "formation"}).find_all("li")
        last_updated = team.find("li", {"class": "grey"}).get_text()

        team_lineup = []
        for player in team_lineup_element:
            team_lineup.append(unidecode(player.get_text().strip()))

        all_team_lineups.append(Team(team_name, team_lineup, last_updated))

    return all_team_lineups


def map_lineups_to_teams(games, lineups):
    for game in games:
        for team in lineups:
            if team.name == team_name_map(game.home_team):
                game.home_team = team
                break

        for team in lineups:
            if team.name == team_name_map(game.away_team):
                game.away_team = team
                break

    return games


def get_for_and_against_stats(games):
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    soup = get_soup(url)
    table_rows = soup.find("table", id="results2023-202491_home_away").find("tbody").find_all("tr")

    for game in games:
        for row in table_rows:
            team_name = row.find("td", {"data-stat": "team"}).get_text().strip()

            # Home
            if team_name_map(team_name) == game.home_team.name:
                home_games_played = float(row.find("td", {"data-stat": "home_games"}).get_text())
                home_goals_for = float(row.find("td", {"data-stat": "home_goals_for"}).get_text())
                home_goals_against = float(row.find("td", {"data-stat": "home_goals_against"}).get_text())
                home_xga = float(row.find("td", {"data-stat": "home_xg_against"}).get_text())

                game.home_team.goals_scored_p90 = home_goals_for / home_games_played
                game.home_team.goals_conceded_p90 = home_goals_against / home_games_played
                game.home_team.total_xga = home_xga / home_games_played

            # Away
            elif team_name_map(team_name) == game.away_team.name:
                away_games_played = float(row.find("td", {"data-stat": "away_games"}).get_text())
                away_goals_for = float(row.find("td", {"data-stat": "away_goals_for"}).get_text())
                away_goals_against = float(row.find("td", {"data-stat": "away_goals_against"}).get_text())
                away_xga = float(row.find("td", {"data-stat": "away_xg_against"}).get_text())

                game.away_team.goals_scored_p90 = away_goals_for / away_games_played
                game.away_team.goals_conceded_p90 = away_goals_against / away_games_played
                game.away_team.total_xga = away_xga / away_games_played

    return games


def get_total_team_xg(games):
    for game in games:
        # Home
        home_url = team_stats_page(game.home_team.name)
        soup = get_soup(home_url)
        stat_table_rows = soup.find("tbody").find_all("tr")
        home_total_xg = scrape_players_xg(stat_table_rows, game.home_team.lineup)
        game.home_team.total_xg = home_total_xg

        # Away
        away_url = team_stats_page(game.away_team.name)
        soup = get_soup(away_url)
        stat_table_rows = soup.find("tbody").find_all("tr")
        away_total_xg = scrape_players_xg(stat_table_rows, game.away_team.lineup)
        game.away_team.total_xg = away_total_xg

    return games


def scrape_players_xg(table, lineup):
    total_xg = 0
    for row in table:
        player = row.find("th", {"data-stat": "player"}).get_text().split()[-1]

        if player:
            players_names = player.split()
            first_name, last_name = players_names[0], players_names[-1]

            if any(unidecode(first_name) in name or unidecode(last_name) in name for name in lineup):
                player_xg = row.find("td", {"data-stat": "xg_per90"}).get_text()

                if player_xg:
                    total_xg += float(player_xg)

    return round(total_xg, 2)


def adjust_teams_xg(games):
    for game in games:
        # For/against xg adjustment
        home_adj_xg = get_xg_average(game.home_team, game.away_team)
        away_adj_xg = get_xg_average(game.away_team, game.home_team)
        game.home_team.adjusted_xg = home_adj_xg
        game.away_team.adjusted_xg = away_adj_xg
        game.total_xg = round(home_adj_xg + away_adj_xg, 2)

    return games


def get_xg_average(team1, team2):
    return round((team1.total_xg
                  + team1.goals_scored_p90
                  + team2.total_xga
                  + team2.goals_conceded_p90) / 4, 2)


def get_goal_data(games):
    for game in games:
        home_xg = game.home_team.adjusted_xg
        away_xg = game.away_team.adjusted_xg

        for goals in range(7):
            home_odds = round(poisson_probability(home_xg, goals), 3)
            away_odds = round(poisson_probability(away_xg, goals), 3)

            game.home_team.goal_data.append(GoalChance(goals, home_odds))
            game.away_team.goal_data.append(GoalChance(goals, away_odds))

    return games


def print_goal_data(games):
    for game in games:
        home_team = game.home_team.name
        away_team = game.away_team.name
        home_xg = game.home_team.adjusted_xg
        away_xg = game.away_team.adjusted_xg
        data = []

        for goals in range(6):
            home_odds = round(poisson_probability(home_xg, goals) * 100, 2)
            away_odds = round(poisson_probability(away_xg, goals) * 100, 2)

            data.append({"Goals": goals,
                         f"{three_letter_abbreviation(home_team)}": f"{home_odds}%",
                         f"{three_letter_abbreviation(away_team)}": f"{away_odds}%"})
        df = pd.DataFrame(data)

        print(df)


def poisson_probability(xg, goal_amount):
    return math.exp(-xg) * (xg ** goal_amount) / math.factorial(goal_amount)


def get_correct_score_odds(games):
    for game in games:
        home_goals_data = game.home_team.goal_data
        away_goals_data = game.away_team.goal_data

        for h_data in home_goals_data:
            for a_data in away_goals_data:
                prob = h_data.probability * a_data.probability
                if prob == 0:
                    prob = "Never gonna happen"
                # else:
                #     prob = round(1 / prob, 2)
                game.correct_score_odds.append(CorrectScore(f"{game.home_team.name} | {game.away_team.name}",
                                                            f"{h_data.goal_amount} - {a_data.goal_amount}",
                                                            prob))

    return games


def print_correct_score_data(games):
    for game in games:
        home_team, away_team = game.correct_score_odds[0].teams.split(" | ")
        data = []

        for score in game.correct_score_odds:
            home_score, away_score = score.score.split(" - ")
            data.append([home_score, away_score, round(1 / score.probability, 2)])

        table_headers = [three_letter_abbreviation(home_team), three_letter_abbreviation(away_team), "Odds"]
        table = tabulate(data, headers=table_headers, tablefmt="fancy_grid")

        print(table)


def get_outcome_odds(games):
    for game in games:
        h_goal_data = game.home_team.goal_data
        a_goal_data = game.away_team.goal_data
        h_win_prob = 0
        a_win_prob = 0
        draw_prob = 0

        for h_data in h_goal_data:
            h_goal = h_data.goal_amount
            h_prob = h_data.probability

            for a_data in a_goal_data:
                a_goal = a_data.goal_amount
                a_prob = a_data.probability

                if h_goal > a_goal:
                    h_win_prob += h_prob * a_prob
                elif h_goal < a_goal:
                    a_win_prob += h_prob * a_prob
                else:
                    draw_prob += h_prob * a_prob

        game.home_team_odds = round(1 / h_win_prob, 2)
        game.away_team_odds = round(1 / a_win_prob, 2)
        game.draw_odds = round(1 / draw_prob, 2)

    return games


def print_outcome_odds(games):
    for game in games:
        home_team = game.home_team.name
        away_team = game.away_team.name

        data = [[game.home_team_odds, game.draw_odds, game.away_team_odds]]
        table_headers = [three_letter_abbreviation(home_team), "Draw", three_letter_abbreviation(away_team)]
        table = tabulate(data, headers=table_headers, tablefmt="fancy_grid")

        print(table)


def get_goals_over_under_odds(games):
    for game in games:
        over_goals = {0.5: 0, 1.5: 0, 2.5: 0, 3.5: 0, 4.5: 0, 5.5: 0}
        under_goals = {0.5: 0, 1.5: 0, 2.5: 0, 3.5: 0, 4.5: 0, 5.5: 0}

        for score in game.correct_score_odds:
            home_score, away_score = map(float, score.score.split(" - "))
            total_score = home_score + away_score

            for goal_value in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]:
                if total_score < goal_value:
                    under_goals[goal_value] += score.probability
                else:
                    over_goals[goal_value] += score.probability

        for goals in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]:
            over_value = over_goals[goals]
            under_value = under_goals[goals]
            game.over_under_odds.append(OverUnder(goals, over_value, under_value))

    return games


def print_over_under_odds(games):
    for game in games:
        data = []

        for odds in game.over_under_odds:
            goal_amount = odds.goals
            over_odds = round(1 / odds.over_probability, 2)
            under_odds = round(1 / odds.under_probability, 2)
            data.append([goal_amount, over_odds, under_odds])

        table_headers = ["Goal Amount", "Over Odds", "Under Odds"]
        table = tabulate(data, table_headers, tablefmt="fancy_grid")

        print(f"                  "
              f"{three_letter_abbreviation(game.home_team.name)} VS {three_letter_abbreviation(game.away_team.name)}")
        print(f"{table}\n")





