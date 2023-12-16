class Team:
    def __init__(self, name, lineup, last_updated):
        self.name = name
        self.lineup = lineup
        self.lineup_last_updated = last_updated
        self.total_xg = 0
        self.total_xga = 0
        self.total_goals_conceded = 0
        self.goals_conceded_p90 = 0
        self.adjusted_xg = 0

    def get_team_name(self):
        return self.name

    def get_lineup(self):
        return self.lineup

    def get_total_xg(self):
        return self.total_xg

    def get_total_xga(self):
        return self.total_xga

    def get_total_goals_conceded(self):
        return self.total_goals_conceded

    def set_total_xg(self, xg):
        self.total_xg = xg

    def set_total_xga(self, xga):
        self.total_xga = xga

    def set_total_goals_conceded(self, total_goals):
        self.total_goals_conceded = total_goals

    def set_total_goals_conceded_p90(self, total_goals):
        self.goals_conceded_p90 = total_goals

    def set_adjusted_xg(self, xg):
        self.adjusted_xg = xg