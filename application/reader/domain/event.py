from datetime import time
from .fight import Fight
class Event():

    def __init__(self, start,  end, rows:list, owner, location):
        self.start = start
        self.location = location
        self.end = end
        self.rows = rows
        self.owner = owner
    
    def __str__(self):
        start = str(self.start)[:-3]+" - "+str(self.end)[:-3]+", "+self.location
        start = start.ljust(54)
        return start+" row count: "+str(len(self.rows))  

    def analyze(self):      
        in_fight = False
        fights = []
        owner = None  
        temp = []
        end = None
        for r in self.rows:
           
            if in_fight:
                temp.append(r)
                if r.type_details == "ExitCombat" or (r.type_details == "Death" and r.target == owner):
                    in_fight = False
                    end = r.timestamp
                    if append_to_last:
                        fights[len(fights)-1].combine_fight(Fight(start,end,location,temp))
                    else:
                        fights.append(Fight(start,end,location,temp))
                    temp.clear()

            elif r.type_details == "EnterCombat":
                in_fight = True
                temp.append(r)
                start = r.timestamp
                if end is not None:
                    diff_to_last = end-start
                    print(diff_to_last)
                    if diff_to_last<0:
                        print(diff_to_last)
                else:
                    append_to_last = False


        
                    

