import requests
from datetime import datetime
from bs4 import BeautifulSoup


def find_games(league_id, date):

    url = f"https://fbref.com/en/matches/{date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")

    for game in league_games:
        h = game.find("td", {"data-stat": "home_team"})
        a = game.find("td", {"data-stat": "away_team"})

        if h and a:
            home_team = h.find("a").get_text()
            away_team = a.find("a").get_text()

            print(home_team)
            print(away_team)


find_games(70, "2023-12-15")

