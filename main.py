import requests
from datetime import datetime
from bs4 import BeautifulSoup
from util import team_name_map
import json


# league id is referencing the id's on fbref
def find_games(league_id, date):
    url = f"https://fbref.com/en/matches/{date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")

    games = []
    for game in league_games:
        h = game.find("td", {"data-stat": "home_team"})
        a = game.find("td", {"data-stat": "away_team"})

        if h and a:
            home_team = h.find("a").get_text()
            away_team = a.find("a").get_text()
            games.append({"home_team": team_name_map(home_team), "away_team": team_name_map(away_team)})

    return games


def find_lineups(games):
    for game in games:
        game["players"] = ["Luke Reed", "John Doe", "testing 123"]

    return games


daily_games = find_games(9, "2023-12-15")


daily_games = find_lineups(daily_games)


print(json.dumps(daily_games, indent=2))


