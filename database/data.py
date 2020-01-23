import sqlite3

class data:
    
    def __init__(self):
        try:
            self.conn=sqlite3.connect('/home/sorjjoon/tika_harj/MyParser/database/data.db', isolation_level=None)
            self.create_tables()
            print("connection successfull")
        except Exception as e:
            print(e)

    def generate_test_players(self):
        c=self.conn.cursor()
        #just a test function so no need to be safe against injection
        for i in range(1,20):
            c.execute("INSERT INTO PLAYER (name) VALUES ('player"+str(i)+"');" )
        c.close

    def get_playerid(self, name: str):
        c=self.conn.cursor()
        c.execute("SELECT id FROM PLAYER WHERE name LIKE ?", [name])
        id = c.fetchall()
        c.close()
        return id

    

    #TODO timestamps
    def insert_match(self,logId: int, round1: bool, round2: bool, round3: bool):
        sql = "INSERT INTO match(round1, round2, round3) VALUES(?,?,?)"
        c = self.conn.cursor()
        c.execute(sql, [round1, round2, round3])
        id = c.lastrowid
        c.close
        return id
        


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
       FOREIGN KEY(logID) REFERENCES log(id),
       timestamp time
       
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



        
