import os
import datetime
from datetime import time
from application.domain.domain import match

class Row():
    #Details can be expanded later if needed (currently contains events and effects)
    def __init__(self, timestamp, source, target, ability_name, details):
        self.time=timestamp
        self.source=source
        self.target=target
        self.ability_name=ability_name
        self.details=details


    def __str__(self):
        return self.time +", "+ self.source +", "+ self.target +", "+ self.ability_name +", "+ self.details

def next_element(row: str):
    element = get_next_element(row)
    return element, row.replace("["+element+"]", "", 1).strip()
#This is an incomplete reader which can be expanded later, depending on the needs of the project
def read_row(row: str):
    timestamp, row = next_element(row)
    source, row = next_element(row)
    target, row = next_element(row)
    ability_name, row = next_element(row)
    details, row = next_element(row)
    return Row(timestamp, source, target, ability_name, details)

    


def parse_log(log_name: str):
    path = "uploads/"+log_name
    matches =[]
    rounds=[]
    player ="" #name of the log_owner
    try:
        with open(path,"r", encoding="iso-8859-1") as f:
            #TODO, if time make file reading work properly
            in_match = False   #true while inside a match, false otherwise
            count = 1
            i =0 #Used for tracking row number. 
            for row in f:
                i+=1
                if in_match:

                    row_object = read_row(row)
                   
                    if "Deserter Detection {3297813328822272}" in row_object.details:     
                        rounds.append(0)        #Determines start of round, TODO win/loss prediction
                        
                    elif "ApplyEffect {836045448945477}: Safe Login Immunity {973870949466372}" in row_object.details: 
                            
                        
                        end = time.fromisoformat(row_object.time)
                        if len(rounds)==3:
                            matches.append(match(start, end,rounds[0], rounds[1],rounds[2], team, opponents, count))
                        else:
                            matches.append(match(start, end,rounds[0], rounds[1], None, team, opponents, count))
                        count+=1    
                        in_match = False
                        rounds=[]

                    else: #finding teammates and enemies. Currently only checking most common occurances (starter buffs, dmg and heal) TODO improve this
                        if row_object.target == row_object.source: # only possible if both are player
                            continue
                            #Starter buffs
                        if "Hunter's Boon" in row_object.ability_name or "Mark of Power" in row_object.ability_name or "Coordination" in row_object.ability_name or "Unnatural Might" in row_object.ability_name:
                            if row_object.target != player and row_object.target not in team and row_object.target:
                                team.append(row_object.target)
                            elif row_object.source not in team and row_object.source != player and row_object.source:
                                team.append(row_object.source)
                            continue

                        if "Damage" in row_object.details:
                            if row_object.target != player and row_object.target not in opponents and row_object.target:
                                opponents.append(row_object.target)
                            elif row_object.source not in opponents and row_object.source != player and row_object.source:
                                opponents.append(row_object.source)
                            continue

                        if "Heal" in row_object.details:
                            if row_object.target != player and row_object.target not in team and row_object.target:
                                team.append(row_object.target)
                            elif row_object.source not in team and row_object.source != player and row_object.source:
                                team.append(row_object.source)
                            continue
                else:
                    if "{3289210509328384}" in row:    #{3289210509328384} is id for Bolster
                        row_object = read_row(row)
                        player = row_object.target #This doesn't change throughout the log ofc, but this is the only guaranteed way to find it
                        start = time.fromisoformat(row_object.time)                       
                        in_match=True
                        team = []
                        opponents = []
        return matches

    except EnvironmentError as r:
        print(r)
    finally:
        f.close()
        print("deleting "+path)
        if os.path.isfile(path) and __name__ != "__main__": #name check for testing TODO remove name check when testing is done
            os.remove(path)



def get_next_element(row: str):
    return row[row.index("[")+1:row.index("]")]




    

