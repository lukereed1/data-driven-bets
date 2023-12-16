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


def get_teams_stats(games):
    for game in games:
        # Home
        home_url = team_stats_page(game.home_team.name)
        soup = get_soup(home_url)

        stat_table_rows = soup.find("tbody").find_all("tr")
        opponent_stats = soup.find(text="Opponent Total").find_parent().find_parent()

        home_total_xg = get_team_xg_per_90(stat_table_rows, game.home_team.lineup)
        home_total_xga = get_team_xg_against_per_90(opponent_stats)
        home_goals_conceded = get_team_goals_conceded(opponent_stats)

        game.home_team.set_total_xg(home_total_xg)
        game.home_team.set_total_xga(home_total_xga)
        game.home_team.set_total_goals_conceded(home_goals_conceded)

        # Away
        away_url = team_stats_page(game.away_team.name)
        soup = get_soup(away_url)

        stat_table_rows = soup.find("tbody").find_all("tr")
        opponent_stats = soup.find(text="Opponent Total").find_parent().find_parent()

        away_total_xg = get_team_xg_per_90(stat_table_rows, game.away_team.lineup)
        away_total_xga = get_team_xg_against_per_90(opponent_stats)
        away_goals_conceded = get_team_goals_conceded(opponent_stats)

        game.away_team.set_total_xg(away_total_xg)
        game.away_team.set_total_xga(away_total_xga)
        game.away_team.set_total_goals_conceded(away_goals_conceded)

    return games


def get_team_xg_per_90(table, lineup):
    total_xg = 0
    for row in table:
        player = row.find("th", {"data-stat": "player"}).get_text().split()[-1]
        players_names = player.split()
        first_name, last_name = players_names[0], players_names[-1]

        if any(unidecode(first_name) in name or unidecode(last_name) in name for name in lineup):
            player_xg = row.find("td", {"data-stat": "xg_per90"}).get_text()
            total_xg += float(player_xg)
    return round(total_xg, 2)


def get_team_xg_against_per_90(stats):
    return stats.find("td", {"data-stat": "xg_per90"}).get_text()


def get_team_goals_conceded(stats):
    return stats.find("td", {"data-stat": "goals"}).get_text()


def get_league_goals_conceded_avg():
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    soup = get_soup(url)
    table_rows = soup.find("table", id="stats_squads_standard_against").find("tbody").find_all("tr")

    total_goals_conceded = 0
    for row in table_rows:
        total_goals_conceded += int(row.find('td', {"data-stat": "goals"}).get_text()) / 20

    return round(total_goals_conceded, 2)
