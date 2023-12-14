import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def team_name_map(name):
    teams = {
        "Nott'ham Forest": "Nottingham Forest",
        "Tottenham": "Tottenham Hotspur"
    }
    return teams.get(name)


def get_team_stats_url(team_name):
    url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    soup = get_soup(url)
    link = soup.find(text=team_name).find_parent().get("href")
    return f"fbref.com{link}"