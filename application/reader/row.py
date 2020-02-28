from datetime import time

# from application import translate_dict
# from application import translate_file_path


class Row():
    # Details can be expanded later if needed (currently contains events and effects)
    __slots__ = ['timestamp', 'source', "target", "ability_name", "row_type",
                 "type_details", "crit", "shielded", "dmg_type", "dmg_heal", "threat"]

    def __init__(self, timestamp, source, target, ability_name, row_type, type_details, crit, shielded, dmg_type, dmg_heal, threat):
        self.timestamp = timestamp
        self.source = source
        self.target = target
        self.ability_name = ability_name
        self.row_type = row_type
        self.type_details = type_details
        self.crit = crit
        self.shielded = shielded
        self.dmg_type = dmg_type
        self.dmg_heal = dmg_heal
        self.threat = threat

    def __str__(self):  # for debugging
        return str(self.timestamp) + ", " + self.source + ", " + self.target + ", " + self.ability_name + ", " + self.type_details + ", crit " + str(self.crit) + ", shielded "+str(self.shielded)+", dmg type " + str(self.dmg_type)+", "+str(self.dmg_heal)+", "+str(self.threat)

    @staticmethod
    def translate(name_with_id: str, translate_dict):
        if not name_with_id.strip():
            return ""
        try: #deal with these bs rows [22:05:01.764] [@Firâksian] [@Firâksian] [Flagship: Orbital Support {3428028147302400}] [ApplyEffect {836045448945477}: Flagship: Orbital Support {3428028147302656}] ()
            last_index= name_with_id.index("}")
        except:
            last_index = len(name_with_id)

        id = name_with_id[name_with_id.index(
            "{")+1:last_index]

        name = translate_dict.get(id.strip())
        
        if name is None:
            
            translate_file_path = "C:\\Users\\joona\\MyParser\\application\\translations.txt"
            with open(translate_file_path, "a", ) as f:
                f.write(
                    "\n"+name_with_id[0:name_with_id.index("{")].strip()+";"+id)
            name = name_with_id[0:name_with_id.index("{")].strip()
            translate_dict[id]=name
        return name

    # Example row:
    # [22:49:49.458] [@Never Back-down] [@Firaksian] [Roaming Mend {3401283385950208}] [ApplyEffect {836045448945477}: Heal {836045448945500}] (11043)
    # [22:00:17.593] [Untamed Scout {4256157971513344}:39360004209710] [@Firaksian] [Assault {2070681042812928}] [ApplyEffect {836045448945477}: Damage {836045448945501}] (0 -dodge {836045448945505}) <1>
    # [22:00:17.592] [Untamed Scout {4256157971513344}:39360004209710] [@Firaksian] [Assault {2070681042812928}] [ApplyEffect {836045448945477}: Damage {836045448945501}] (3369 kinetic {836045448940873} (3369 absorbed {836045448945511})) <3369>
    # [17:24:58.536] [@Firâksîân] [@Jhagonn] [Electro Net {3066456325488640}] [ApplyEffect {836045448945477}: Damage {836045448945501}] (733 energy {836045448940874} -shield {836045448945509} (1084 absorbed {836045448945511})) <733>
    # For this row,
    # time = 22:49:49.458
    # source = @Never Back-down
    # target = @Firaksian
    # ability_name = Roaming Mend
    # details = ApplyEffect {836045448945477}: Heal {836045448945500}
    @staticmethod
    def read_row(row: str, translate_dict):
        try:
            
            split_row = row.split("] [")
            timestamp = time.fromisoformat(split_row[0][1:])
            source = split_row[1]
            target = split_row[2]
            ability_name = Row.translate(split_row[3], translate_dict)
            type_parts = split_row[4].split("}:")
            row_type = Row.translate(type_parts[0], translate_dict)
            #bs rows, [22:29:35.987] [@Bardsalger] [@Firaksian] [Concussive Round {1682579208011776}] [ApplyEffect {836045448945477}: Asleep [Mental] {1682579208012034}] ()
            if "[" in type_parts[1]:
                
                more_parts = type_parts[1].replace("[","").replace("]","").split("(")
                
                type_details = Row.translate(more_parts[0], translate_dict)
            else:
                more_parts= type_parts[1].split("]")
                type_details = Row.translate(more_parts[0], translate_dict)
                
            dmg_heal, crit, dmg_type, shielded, threat = Row.translate_dmg(
                more_parts[1], type_details, translate_dict)

            return Row(timestamp, source, target, ability_name, row_type, type_details, crit, shielded, dmg_type, dmg_heal, threat)

        # will happen only if the user has modified a row for some reason (or if the row was never valid, such as a random text file)
        except Exception as e:
            raise e
            return None
    # (0 -dodge {836045448945505}) <1>
    @staticmethod
    def translate_dmg(dmg_details, type_details, translate_dict):
        # (3369 kinetic {836045448940873} (3369 absorbed {836045448945511})) <3369>
        # print(without_threat_parts)
        if type_details == "Damage":
            without_threat = dmg_details[dmg_details.index(
                "(")+1:dmg_details.index(")")]
            without_threat_parts = without_threat.split(" ")
            if len(without_threat_parts) >= 6:
                try:
                    shielded = "-shield" == Row.translate(
                        without_threat_parts[5], translate_dict)
                except:
                    shielded = "-shield" == Row.translate(
                        without_threat_parts[4], translate_dict)
            else:
                shielded = False
            size = without_threat_parts[0]
            try:
                crit_index = size.index("*")
                crit = True
                dmg_heal = int(size[0:crit_index])
            except ValueError as e:
                crit = False
                dmg_heal = int(size)
            try:
                dmg_type = Row.translate(
                    without_threat_parts[2], translate_dict)
            except:
                if dmg_heal == 0:
                    dmg_type = "miss"
                else:
                    dmg_type = None
            try:
                threat = int(dmg_details[dmg_details.index(
                    "<")+1:dmg_details.index(">")])
            except ValueError as r:
                threat = 0

        elif type_details == "Heal":
            dmg_type = None
            shielded = False
            without_threat = dmg_details[dmg_details.index(
                "(")+1:dmg_details.index(")")]
            without_threat_parts = without_threat.split(" ")
            try:
                threat = int(dmg_details[dmg_details.index(
                    "<")+1:dmg_details.index(">")])
            except ValueError as r:
                threat = 0
            size = without_threat_parts[0]
            try:
                crit_index = size.index("*")
                crit = True
                dmg_heal = int(size[0:crit_index])
            except ValueError as e:
                crit = False
                dmg_heal = int(size)
        elif type_details == "EnterCombat":
            crit = False
            dmg_heal = 0
            threat = 0
            dmg_type = dmg_details[dmg_details.index(
                "(")+1:dmg_details.index(")")] #place
            shielded = False

        else:
            crit = False
            dmg_heal = 0
            threat = 0
            dmg_type = None
            shielded = False
        return dmg_heal, crit, dmg_type, shielded, threat


if __name__ == "__main__":
    import os
    from timeit import default_timer as timer
    
    path = "C:\\Users\\joona\\Documents\\Star Wars - The Old Republic\\CombatLogs"
    files = os.listdir(path)
    i = 1
    start = timer()
    translate_dict = {}
    try:
        translate_file_path = "C:\\Users\\joona\\MyParser\\application\\translations.txt"

        with open(translate_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                
                if len(line)>2:
                    parts = line.split(";")  # name, id
                    # print(parts)
                    translate_dict[parts[1].strip()] = parts[0]

    except EnvironmentError as r:
        print(r)
    end = timer()
    print(end - start)
    print("dict")
    big_start = timer()
    sizes = []
    lengths = []
    import sys
    for x in files:
       
        if os.path.isfile("C:\\Users\\joona\\Documents\\Star Wars - The Old Republic\\CombatLogs\\"+x):
            i = 1
            rows = []
            start = timer()
            print(x)
            with open("C:\\Users\\joona\\Documents\\Star Wars - The Old Republic\\CombatLogs\\"+x, "r", encoding="iso-8859-1") as f:

                for line in f:
                    if len(line)<10:
                        continue
                    try:
                        r = Row.read_row(line, translate_dict)
                        rows.append(r)
                        i += 1
                    except Exception as e:
                        print(line)
                        print(i)
                        raise e
                #sizes.append(sys.getsizeof(rows))
                        

            end = timer()
            lengths.append(end - start)
        else:
            print(x)
    big_end  = timer()
    print("max parse time")
    print(max(lengths))
    print(big_end-big_start)
    
    print("dict size")
    #print(sys.getsizeof(translate_dict))
