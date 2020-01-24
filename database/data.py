import sqlite3

class data:
    
    def __init__(self):
        try:
            self.conn=sqlite3.connect('data.db', isolation_level=None, check_same_thread=False)
            self.create_tables()
            print("connetion successful")
        except Exception as e:
            print(e)

            
    def get_log_ids(self, user_id: int):
        c=self.conn.cursor()
        c.execute("SELECT id FROM log WHERE ownerID = ?", [user_id])
        id = c.fetchall()
        c.close()
        return id

    def insert_log(self, owner_id: int, matches: list):
        c=self.conn.cursor()
        #OWnerID always int, so no chance of injection
        c.execute("INSERT INTO Log(OwnerID) Values("+str(owner_id)+")")

        self.conn.commit()
        print("log added")
        log_id = c.lastrowid
        c.close()
        for tuples in matches:
            if(len(tuples)!=3):
                raise ValueError('Matches must be represented by a tuple with length 3')
            else:
                self.__insert_match(log_id,tuples[0],tuples[1],tuples[2])
                print("match added")



    def delete_log(self, log_id: int):
        c=self.conn.cursor()
        try:
            #TODO match_player
            c.execute("DELETE FROM Match WHERE logID ="+str(log_id))
            c.execute("DELETE FROM Log WHERE id = "+str(log_id))
            self.conn.commit()
            print("Deletion successfull")
            c.close()
        except Exception as e:
            
            print("Deletion failed")
            print(e)
            self.conn.rollback()
            c.close()

        

    def generate_test_data(self):
        c=self.conn.cursor()
        #just a test function so no need to be safe against injection
        c.execute("INSERT INTO USER(username, password) VALUES('test','test')")
        for i in range(1,20):
            c.execute("INSERT INTO PLAYER (name) VALUES ('player"+str(i)+"');" )
            print("INSERT INTO PLAYER (name) VALUES ('player"+str(i)+"');")
            
        self.conn.commit()            
        c.close

    def get_playerid(self, name: str):
        c=self.conn.cursor()
        c.execute("SELECT id FROM PLAYER WHERE name LIKE ?", [name])
        id = c.fetchall()
        c.close()
        return id

    

    #TODO timestamps
    def __insert_match(self, log_id: int, round1: bool, round2: bool, round3: bool):
        sql = "INSERT INTO match(logID, round1, round2, round3) VALUES(?,?,?,?)"
        c = self.conn.cursor()
        c.execute(sql, [log_id, round1, round2, round3])
        self.conn.commit()
        id = c.lastrowid
        c.close
        return id
        
    def get_matches(self, log_ids):
        # adding correct number of ? to string
        sql = "SELECT round1, round2, round3 FROM match WHERE match.logID in ({s})".format(s=','.join(['?']*len(log_ids)))
        c = self.conn.cursor()
        c.execute(sql, log_ids)
        wins = c.fetchall()
        c.close()
        return wins


    def create_tables(self):
        tables ="""
CREATE TABLE IF NOT EXISTS User (
       username varchar(20) NOT NULL,
       password varchar(30) NOT NULL,
       id INTEGER PRIMARY KEY NOT NULL
       
);



CREATE TABLE IF NOT EXISTS Log (
       id INTEGER PRIMARY KEY NOT NULL,
       ownerID int NOT NULL,
       log BLOB,
       date DATE,       
       FOREIGN KEY(ownerID) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Player (
       name varchar(20) NOT NULL,
       id INTEGER PRIMARY KEY NOT NULL
       
);

CREATE TABLE IF NOT EXISTS Match (
       id INTEGER PRIMARY KEY NOT NULL,
       round1 boolean NOT NULL,
       round2 boolean NOT NULL,
       round3 boolean,
       logID int,
       timestamp DATETIME, 
       FOREIGN KEY(logID) REFERENCES log(id)
            
);


CREATE TABLE IF NOT EXISTS match_player (
       matchID int,
       playerID int,
       side boolean NOT NULL,
       FOREIGN KEY(matchID) REFERENCES match(id),
       FOREIGN KEY(playerID) REFERENCES player(id)
);
       """
        c = self.conn.cursor()
        
        c.executescript(tables)
        c.close



        
