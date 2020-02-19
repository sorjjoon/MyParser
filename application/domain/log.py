from sqlalchemy.types import  Date
class log():
    def __init__(self,id:int, date: Date,char:str, matches = [], note=None):
        self.id=id
        self.date=date
        self.matches=matches
        self.char = char
        self.note = note

    def set_matches(self, matches:list):
        self.matches=matches

    def __str__(self):
        return str(self.date)
