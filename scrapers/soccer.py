from util import team_name_map, get_soup, get_team_stats_url, serialize
from models.game import Game
from unidecode import unidecode
import json


def find_games(league_id, date):
    url = f"https://fbref.com/en/matches/{date}"
    soup = get_soup(url)

    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")
    games = []

    for game in league_games:
        home = game.find("td", {"data-stat": "home_team"})
        away = game.find("td", {"data-stat": "away_team"})

        if home and away:
            home_team = home.find("a").get_text()
            away_team = away.find("a").get_text()
            game = Game(home_team=home_team, away_team=away_team, date=date)
            games.append(game)

    return games


def find_lineups(games):
    url = "https://www.fantasyfootballscout.co.uk/team-news/"
    soup = get_soup(url)

    for game in games:
        # Targets divs that desired team names inside of
        home_formation_div = (soup.find(text=team_name_map(game.home_team.name))
                              .find_parent().find_parent()
                              .find_parent().find_next_sibling())

        away_formation_div = (soup.find(text=team_name_map(game.away_team.name))
                              .find_parent().find_parent()
                              .find_parent().find_next_sibling())

        if home_formation_div and away_formation_div:
            # Grabs all list items that have player names
            home_lineup = home_formation_div.find_all("li")
            away_lineup = away_formation_div.find_all("li")

            # Appends players to team lineup
            for player in home_lineup:
                game.home_team.lineup.append(unidecode(player.get_text()))

            for player in away_lineup:
                game.away_team.lineup.append(unidecode(player.get_text()))

    return games


def find_teams_xg(games):
    for game in games:
        home_url = get_team_stats_url(game.home_team.name)
        away_url = get_team_stats_url(game.away_team.name)

        home_lineup = [s.strip() for s in game.home_team.lineup]
        away_lineup = [s.strip() for s in game.away_team.lineup]

        soup = get_soup(home_url)

        stat_table_rows = soup.find("tbody").find_all("tr")

        print(home_lineup)
        for row in stat_table_rows:
            player = row.find("th", {"data-stat": "player"}).get_text().split()[-1]

            if player in home_lineup:
                print(player)






