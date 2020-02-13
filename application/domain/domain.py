
from sqlalchemy.types import Time, Date


class log():
    def __init__(self,id:int, date: Date,char:str, matches = []):
        self.id=id
        self.date=date
        self.matches=matches
        self.char = char

    def set_matches(self, matches:list):
        self.matches=matches

    def __str__(self):
        return str(self.date)

class char():
    def __init__(self, id:int, name:str, char_class="-", server="-" ):
        self.id = id
        self.name = name
        if char_class is None:
            self.char_class = " - "
        else:
            self.char_class = char_class
        if server is None:
            self.server = " - "
        else:
            self.server=server


class match():
    def __init__(self,start: Time, end: Time, round1, round2, round3, team: list, opponent: list, number = 0, error = None, note=None):

        self.start=start
        self.end=end
        self.round1=round1
        self.round2= round2
        self.round3=round3
        self.team=team
        self.opponent=opponent
        self.note=note
        #used by jinja templates
        self.error = error
        self.start_string=str(start)[:-10]
        self.end_string=str(end)[:-10]
        self.number=number
        self.team_string=str(self.team)[:-1][1:].replace("'","")
        self.opponent_string=str(self.opponent)[:-1][1:].replace("'","")

    def validate(self): #validate that this match has valid round 1, 2 and 3 values
        if self.round3 is None:
            if self.round2 == self.round1:
                return True
            else:
                self.error = "Round 3 wasn't played, rounds 1 and 2 must be the same"
                return False
        else:
            if self.round1 != self.round2:
                return True
            else:
                self.error = "Round 3 was played, rounds 1 and 2 can't be the same"
                return False
            


    def set_rounds(self, round1, round2, round3=None):
        self.round1=round1
        self.round2=round2
        self.round3=round3




