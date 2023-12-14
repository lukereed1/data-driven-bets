from models.team import Team


class Game:
    def __init__(self, home_team, away_team, date):
        self.home_team = Team(home_team)
        self.away_team = Team(away_team)
        self.date = date


