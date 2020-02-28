

class Fight():
    def __init__(self, start,  end, location, rows:list):
        self.start = start
        self.location = location
        self.end = end
        self.rows = rows

    def combine_fight(self, later_fight):
        self.rows+=later_fight.rows