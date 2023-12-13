from util import team_name_map, get_soup
import json
from models.game import Game


# Finds all games for a given date and league
def find_games(league_id, date):
    url = f"https://fbref.com/en/matches/{date}"
    soup = get_soup(url)
    league_games = soup.find("div", id=f"all_sched_2023-2024_{league_id}").find_all("tr")

    games = []
    for game in league_games:
        h = game.find("td", {"data-stat": "home_team"})
        a = game.find("td", {"data-stat": "away_team"})

        if h and a:
            home_team = h.find("a").get_text()
            away_team = a.find("a").get_text()
            game = Game(home_team=home_team, away_team=away_team, date=date)
            games.append(game)

    return games


def find_lineups(games):

    for game in games:
        game["players"] = ["Luke Reed", "John Doe", "testing 123"]

    return games


daily_games = find_games(9, "2023-12-15")



json = json.dumps(daily_games, indent=2, default=lambda obj: obj.__dict__)

print(json)


