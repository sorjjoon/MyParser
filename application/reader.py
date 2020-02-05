import os
from datetime import time
from application.domain.domain import match




def parse_log(log_name: str):
    path = "uploads/"+log_name
    matches =[]
    rounds=[]
    try:
        with open(path,"r", encoding="iso-8859-1") as f:
            #TODO, if time make file reading work properly
            in_match = False   #true while inside a match, false otherwise
            count = 1
            i =0 #Used for tracking row number. 
            for line in f:
                i+=1
                if in_match:
                    
                    if "ApplyEffect {836045448945477}: Deserter Detection {3297813328822272}" in line:     # {836045448945477} is id for  Deserter Detection
                        rounds.append(0)        #Determines start of round, TODO win/loss prediction
                        
                    elif "ApplyEffect {836045448945477}: Safe Login Immunity {973870949466372}" in line: 
                            
                        
                        end = time.fromisoformat(get_next_element(line))
                        if len(rounds)==3:
                            matches.append(match(start, end,rounds[0], rounds[1],rounds[2], [], [], count))
                        else:
                            matches.append(match(start, end,rounds[0], rounds[1], None, [], [], count))
                        count+=1    
                        in_match = False
                        rounds=[]                                

                else:
                    if "{3289210509328384}" in line:    #{3289210509328384} is id for Bolster
                        start = time.fromisoformat(get_next_element(line))
                       
                        in_match=True
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



#for testing
if __name__ == "__main__":
    parse_log("combat_2020-01-25_00_03_38_196188.txt")
    


