from util import team_name_map, get_soup, team_stats_page
from models.game import Game
from models.team import Team
from unidecode import unidecode
from util import serialize
import json


def get_games_by_date(league_id, date):
    url = f"https://fbref.com/en/matches/{date}"
    soup = get_soup(url)
    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")
    games = []

    if league_games:
        try:
            for game in league_games:
                home = game.find("td", {"data-stat": "home_team"})
                away = game.find("td", {"data-stat": "away_team"})
                time = game.find("td", {"data-stat": "start_time"})

                if home and away:
                    home_team = home.find("a").get_text()
                    away_team = away.find("a").get_text()
                    start_time = time.find("span", {"class": "venuetime"}).get_text()

                    game = Game(home_team, away_team, date, start_time)
                    games.append(game)
        except Exception as e:
            print(f"Problem finding one or more games: {e}")
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
            if team.get_team_name() == team_name_map(game.home_team):
                game.home_team = team
                break

        for team in lineups:
            if team.get_team_name() == team_name_map(game.away_team):
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

            if team_name_map(team_name) == game.home_team.name:
                home_games_played = float(row.find("td", {"data-stat": "home_games"}).get_text())
                home_goals_for = float(row.find("td", {"data-stat": "home_goals_for"}).get_text())
                home_goals_against = float(row.find("td", {"data-stat": "home_goals_against"}).get_text())
                home_xga = float(row.find("td", {"data-stat": "home_xg_against"}).get_text())

                game.home_team.set_goals_scored_p90(home_goals_for / home_games_played)
                game.home_team.set_goals_conceded_p90(home_goals_against / home_games_played)
                game.home_team.set_total_xga(home_xga / home_games_played)
                game.home_team.set_total_goals_scored(home_goals_for)
                game.home_team.set_total_goals_conceded(home_goals_against)

            elif team_name_map(team_name) == game.away_team.name:
                away_games_played = float(row.find("td", {"data-stat": "away_games"}).get_text())
                away_goals_for = float(row.find("td", {"data-stat": "away_goals_for"}).get_text())
                away_goals_against = float(row.find("td", {"data-stat": "away_goals_against"}).get_text())
                away_xga = float(row.find("td", {"data-stat": "away_xg_against"}).get_text())

                game.away_team.set_goals_scored_p90(away_goals_for / away_games_played)
                game.away_team.set_goals_conceded_p90(away_goals_against / away_games_played)
                game.away_team.set_total_xga(away_xga / away_games_played)
                game.away_team.set_total_goals_scored(away_goals_for)
                game.away_team.set_total_goals_conceded(away_goals_against)

    return games


def get_total_team_xg(games):
    for game in games:
        # Home
        home_url = team_stats_page(game.home_team.name)
        soup = get_soup(home_url)
        stat_table_rows = soup.find("tbody").find_all("tr")
        home_total_xg = scrape_players_xg(stat_table_rows, game.home_team.lineup)
        game.home_team.set_total_xg(home_total_xg)

        # Away
        away_url = team_stats_page(game.away_team.name)
        soup = get_soup(away_url)
        stat_table_rows = soup.find("tbody").find_all("tr")
        away_total_xg = scrape_players_xg(stat_table_rows, game.away_team.lineup)
        game.away_team.set_total_xg(away_total_xg)

    return games


def scrape_players_xg(table, lineup):
    total_xg = 0
    for row in table:
        player = row.find("th", {"data-stat": "player"}).get_text().split()[-1]
        players_names = player.split()
        first_name, last_name = players_names[0], players_names[-1]

        if any(unidecode(first_name) in name or unidecode(last_name) in name for name in lineup):
            player_xg = row.find("td", {"data-stat": "xg_per90"}).get_text()
            total_xg += float(player_xg)
    return round(total_xg, 2)


def adjust_teams_xg(games):
    home_goals_conceded, away_goals_conceded = get_league_goals_conceded_avg()

    for game in games:
        # xg / xga average
        home_xg = (game.home_team.get_total_xg() + game.away_team.get_total_xga()) / 2
        away_xg = (game.away_team.get_total_xg() + game.home_team.get_total_xga()) / 2
        game.home_team.set_adjusted_xg_avgs(home_xg)
        game.away_team.set_adjusted_xg_avgs(away_xg)

        # For/against xg adjustment
        home_adj_xg = get_xg_average(game.home_team, game.away_team)
        away_adj_xg = get_xg_average(game.away_team, game.home_team)
        game.home_team.set_adjusted_xg(home_adj_xg)
        game.away_team.set_adjusted_xg(away_adj_xg)
    return games


def get_league_goals_conceded_avg():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    soup = get_soup(url)
    table_rows = soup.find("table", id="results2023-202491_home_away").find("tbody").find_all("tr")

    home_total_goals_conceded = 0
    away_total_goals_conceded = 0

    for row in table_rows:
        home_total_goals_conceded += float(row.find('td', {"data-stat": "home_goals_against"}).get_text())
        away_total_goals_conceded += float(row.find('td', {"data-stat": "away_goals_against"}).get_text())
    return round(home_total_goals_conceded / 20, 2), round(away_total_goals_conceded / 20, 2)


def get_xg_average(team1, team2):
    return round((team1.get_total_xg()
            + team1.get_goals_scored_p90()
            + team2.get_total_xga()
            + team2.get_goals_conceded_p90()) / 4, 2)


def get_defensive_adjustment_factor(team, league_avg_goals_conceded):
    return round((float(team.get_total_goals_conceded()) / league_avg_goals_conceded), 2)

