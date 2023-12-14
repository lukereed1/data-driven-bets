from models.team import Team


class Game:
    def __init__(self, home_team, away_team, date, time):
        self.date = date
        self.time = time
        self.home_team = Team(home_team)
        self.away_team = Team(away_team)



