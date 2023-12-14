from util import team_name_map, get_soup
from models.game import Game
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
            game = Game(home_team=team_name_map(home_team), away_team=team_name_map(away_team), date=date)
            games.append(game)
    return games


def find_lineups(games):
    url = "https://www.fantasyfootballscout.co.uk/team-news/"
    soup = get_soup(url)

    for game in games:
        home_formation_div = soup.find(text=game.home_team).find_parent().find_parent().find_parent().find_next_sibling()
        away_formation_div = soup.find(text=game.away_team).find_parent().find_parent().find_parent().find_next_sibling()

        if home_formation_div and away_formation_div:
            home_lineup = home_formation_div.find_all("li")
            away_lineup = away_formation_div.find_all("li")

            for player in home_lineup:
                game.home_lineup.append(player.get_text())

            for player in away_lineup:
                game.away_lineup.append(player.get_text())

    return games
