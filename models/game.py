class Game:
    def __init__(self, home_team, away_team, date):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.home_team_lineup = []
        self.away_team_lineup = []

    def set_home_lineup(self, lineup):
        self.home_team_lineup = lineup

    def set_away_lineup(self, lineup):
        self.away_team_lineup = lineup
