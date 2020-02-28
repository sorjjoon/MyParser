import os
from datetime import time
from row import Row
from domain.event import Event 
from domain.fight import Fight




def detect_event(start, end, rows, owner, location):
    return Event(start, end, rows, owner, location)
    





def parse_log(log_name: str, translate_dict):
    #path = "uploads/"+log_name
    path = "C:\\Users\\joona\\Documents\\Star Wars - The Old Republic\\CombatLogs\\"+log_name
    owner = None  # name of the log_owner
    temp = []
    events = [] 
    
    start = None
    location = None
    i=0
  
    with open(path, "r", encoding="iso-8859-1") as f:
        for line in f:
            i+=1
            r = Row.read_row(line, translate_dict)
            if "safe" in r.type_details:
                print(r)
            if start is None:
                start = r.timestamp
            
            temp.append(r)

            if r.type_details == "EnterCombat" and location is None:
                print(r)
                location = r.dmg_type


            if r.type_details == "Safe Login Immunity" and r.row_type == "ApplyEffect":
                end = r.timestamp
                print("moi")
                print(len(temp))
                if owner is None:
                    owner = r.target

                if location is not None: #location is none if no fights
                    events.append(detect_event(start, end, temp, owner, location))
                temp = []
                location = None
                start = None
    return events

    
    

   # finally:
        # delete file after it's been read
   #    f.close()

    #    if os.path.isfile(path) and  __name__ != "__main__":
      #      pass
    #        #os.remove(path)
            #print("deleting "+path)
    #    return events



if __name__ == "__main__":
    translate_dict = {}

    translate_file_path = "C:\\Users\\joona\\MyParser\\application\\translations.txt"

    with open(translate_file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            if len(line)>2:
                parts = line.split(";")  # name, id
                # print(parts)
                translate_dict[parts[1].strip()] = parts[0]

    a= parse_log("combat_2020-01-18_21_16_29_443043.txt", translate_dict)
    print(len(a))
    for x in a:
        print(x)