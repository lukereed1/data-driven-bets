class Team:
    def __init__(self, name):
        self.name = name
        self.lineup = []
        self.lineup_date = None
        self.total_xG = 0

    def set_total_xg(self):
        print("test")
