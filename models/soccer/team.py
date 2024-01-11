class Team:
    def __init__(self, name, lineup, last_updated):
        self.name = name
        self.lineup = lineup
        self.lineup_last_updated = last_updated
        self.total_xg = 0
        self.total_xga = 0
        self.goals_scored_p90 = 0
        self.goals_conceded_p90 = 0
        self.adjusted_xg = 0
        self.goal_data = []

