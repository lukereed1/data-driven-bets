class Team:
    def __init__(self, name):
        self.name = name
        self.lineup = []
        self.lineup_date = None
        self.total_xg = 0
        self.total_xg_against = 0

    def set_total_xg(self, xg):
        self.total_xg = xg

    def set_total_xg_against(self, xga):
        self.total_xg_against = xga
