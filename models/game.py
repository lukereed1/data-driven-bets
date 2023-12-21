class Game:
    def __init__(self, home_team, away_team, date, time):
        self.date = date
        self.time = time
        self.home_team = home_team
        self.away_team = away_team
        self.total_xg = 0
        self.correct_score_odds = []
        self.home_team_odds = 0
        self.away_team_odds = 0
        self.draw_odds = 0


