class Team:
    def __init__(self, name):
        self.name = name
        self.lineup = []
        self.lineup_date = None
        self.total_xg = 0

    def set_total_xg(self, xg):
        self.total_xg = xg
