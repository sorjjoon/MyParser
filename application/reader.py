import os
import datetime
from datetime import time
from application.domain.domain import match
from application.domain.player import Player


class Row():
    #Details can be expanded later if needed (currently contains events and effects)
    def __init__(self, timestamp, source, target, ability_name, details):
        self.time=timestamp
        self.source=source
        self.target=target
        self.ability_name=ability_name
        self.details=details


    def __str__(self): #for debugging
        return self.time +", "+ self.source +", "+ self.target +", "+ self.ability_name +", "+ self.details

def next_element(row: str):
    element = get_next_element(row)
    return element, row.replace("["+element+"]", "", 1).strip()

# Example row: 
# [22:49:49.458] [@Never Back-down] [@Firaksian] [Roaming Mend {3401283385950208}] [ApplyEffect {836045448945477}: Heal {836045448945500}] (11043)
# For this row,
# time = 22:49:49.458
# source = @Never Back-down
# target = @Firaksian
# ability_name = Roaming Mend
# details = ApplyEffect {836045448945477}: Heal {836045448945500}
def read_row(row: str):
    try:
        timestamp, row = next_element(row)
        source, row = next_element(row)
        target, row = next_element(row)
        ability_name, row = next_element(row)
        details, row = next_element(row)
        return Row(timestamp, source, target, ability_name, details)

    except: #will happen only if the user has modified a row for some reason
        return None

    
def find_team_opponent(row_object:Row, team:list, opponents:list, owner):
    if row_object.target == row_object.source: #saves time
        return

        #Starter buffs hunters, mark, Coordination and might are the diffrent types of buffs players can apply to their team mates (and only their team mates)"
    if "Hunter's Boon" in row_object.ability_name or "Mark of Power" in row_object.ability_name or "Coordination" in row_object.ability_name or "Unnatural Might" in row_object.ability_name:
        
        #appending to team the target or source that is not owner (and not already in the list)
        if row_object.target != owner and row_object.target not in team and row_object.target:
            team.append(row_object.target)
        elif row_object.source not in team and row_object.source != owner and row_object.source:
            team.append(row_object.source)
        return

        #appending to enemies the target or source that is not owner (and not already in the list)
    if "Damage" in row_object.details:
        if row_object.target != owner and row_object.target not in opponents and row_object.target:
            opponents.append(row_object.target)
        elif row_object.source not in opponents and row_object.source != owner and row_object.source:
            opponents.append(row_object.source)
        return

        #appending to team list, the row target or souce, depending on which is not owner (and not already in the list)
    if "Heal" in row_object.details:
        if row_object.target != owner and row_object.target not in team and row_object.target:
            team.append(row_object.target)
        elif row_object.source not in team and row_object.source != owner and row_object.source:
            team.append(row_object.source)
        return
    

def parse_log(log_name: str):
    path = "uploads/"+log_name
    matches =[]
    rounds=[]
    owner =None #name of the log_owner
    try:
        with open(path,"r", encoding="iso-8859-1") as f:
            in_match = False   #true while inside a match, false otherwise
            match_number = 1   #used for tracking match number
            
            for row in f:
                
                if in_match:    #saves time, read only rows while we are in a match (there might be a lot of rows between matches)

                    row_object = read_row(row)

                    #deserter detection is applied to owner at the start of a round
                    if "Deserter Detection {3297813328822272}" in row_object.details:     
                        rounds.append(0)        #Determines start of round

                    #Safe Login immunity means a loading screen (a game has ended)    
                    elif "ApplyEffect {836045448945477}: Safe Login Immunity {973870949466372}" in row_object.details: 
                            
                        
                        end = time.fromisoformat(row_object.time)
                        if len(rounds)==3:
                            matches.append(match(start, end,rounds[0], rounds[1],rounds[2], team, opponents, match_number))
                        else:
                            matches.append(match(start, end,rounds[0], rounds[1], None, team, opponents, match_number))
                        match_number+=1    
                        in_match = False
                        rounds=[]

                    else: 
                        #find out, if we can guess an opponent or team mates name from the row, and append it to the correct list
                        find_team_opponent(row_object, team, opponents, owner)
                        
                else:
                    if "{3289210509328384}" in row:    #{3289210509328384} is id for Bolster (notes the start of a game)
                        row_object = read_row(row)
                        owner = row_object.target #player means log owner
                        start = time.fromisoformat(row_object.time)                       
                        in_match=True
                        team = []
                        opponents = []
                        
        return matches, owner

    except EnvironmentError as r:
        print(r)
    finally:
        #delete file after it's been read
        f.close()
        print("deleting "+path)
        if os.path.isfile(path): 
            os.remove(path)



def get_next_element(row: str):
    return row[row.index("[")+1:row.index("]")]




    

