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