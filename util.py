import requests
import json
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def serialize(self):
    return json.dumps(self, indent=4, default=lambda obj: obj.__dict__)


def team_name_map(name):
    teams = {
        "Nott'ham Forest": "Nottingham Forest",
        "Tottenham": "Tottenham Hotspur",
        "Sheffield Utd": "Sheffield United",
        "Newcastle Utd": "Newcastle United",
        "Manchester Utd": "Manchester United",
        "West Ham": "West Ham United",
        "Wolves": "Wolverhampton Wanderers",
        "Brighton": "Brighton and Hove Albion"
    }
    return teams.get(name, name)


def team_stats_page(name):
    stats_page = {
        "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
        "Arsenal": "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
        "Aston Villa": "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
        "Manchester City": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
        "Tottenham Hotspur": "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
        "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
        "Newcastle United": "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
        "Brighton and Hove Albion": "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
        "West Ham United": "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
        "Fulham": "https://fbref.com/en/squads/fd962109/Fulham-Stats",
        "Brentford": "https://fbref.com/en/squads/cd051869/Brentford-Stats",
        "Chelsea": "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
        "Wolverhampton Wanderers": "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats",
        "Bournemouth": "https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats",
        "Crystal Palace": "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
        "Nottingham Forest": "https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats",
        "Everton": "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
        "Luton Town": "https://fbref.com/en/squads/e297cd13/Luton-Town-Stats",
        "Burnley": "https://fbref.com/en/squads/943e8050/Burnley-Stats",
        "Sheffield United": "https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
    }
    return stats_page.get(name)


# def get_team_stats_url(team_name):
#     url = "https://fbref.com/en/comps/9/Premier-League-Stats"
#     soup = get_soup(url)
#     link = soup.find(text=team_name).find_parent().get("href")
#     return f"https://www.fbref.com{link}"
