import os

#This is an incomplete file reader. It has only the functionality that is required for this project
#atm this will return true if read line indicates a started round
def __readline(line: str):
    return "ApplyEffect {836045448945477}: Deserter Detection" in line



def parse_log(log_name: str):
    path = "uploads/"+log_name
    matches =[]
    rounds=[]
    try:
        with open(path,"r", encoding="iso-8859-1") as f:
            #TODO, if time make file reading work properly
            in_match = False   #true while inside a match, false otherwise
            i =0
            for line in f:
                i+=1
                if in_match:
                    
                    if "ApplyEffect {836045448945477}: Deserter Detection {3297813328822272}" in line:     # {836045448945477} is id for  Deserter Detection
                        rounds.append(0)        #Determines start of round, TODO win/loss prediction
                        
                    elif "ApplyEffect {836045448945477}: Safe Login Immunity {973870949466372}" in line: 
                        print(i)    
                        matches.append(rounds)
                        rounds=[]
                        #print(str(i)+"      "+line)
                        in_match = False                                

                else:
                    if "{3289210509328384}" in line:    #{3289210509328384} is id for Bolster
                       # print(line)
                        in_match=True
        return matches

    except EnvironmentError as r:
        print(r)
    finally:
        f.close()
        print("deleting "+path)
        if os.path.isfile(path) and __name__ != "__main__": #name check for testing
            os.remove(path)


#for testing
if __name__ == "__main__":
    parse_log("combat_2020-01-25_00_03_38_196188.txt")
    


