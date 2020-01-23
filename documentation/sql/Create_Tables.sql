CREATE TABLE IF NOT EXISTS User (
       username varchar(20) NOT NULL,
       password varchar(30) NOT NULL,
       id INTEGER PRIMARY KEY NOT NULL
       
);



CREATE TABLE IF NOT EXISTS Log (
       id INTEGER PRIMARY KEY NOT NULL,
       ownerID int NOT NULL,
       date date NOT NULL,       
       FOREIGN KEY(ownerID) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Player (
       name varchar(20) NOT NULL,
       id INTEGER PRIMARY KEY NOT NULL
       
);

CREATE TABLE IF NOT EXISTS Match (
       id INTEGER PRIMARY KEY NOT NULL,
       round1 boolean,
       round2 boolean,
       round3 boolean,
       timestamp time
       
);

CREATE TABLE IF NOT EXISTS match_log (
	    matchID INTEGER PRIMARY KEY NOT NULL,
	    logID int,
        FOREIGN KEY(matchID) REFERENCES match(id),
        FOREIGN KEY(logID) REFERENCES log(id)
);

CREATE TABLE IF NOT EXISTS match_player (
       matchID INTEGER PRIMARY KEY NOT NULL,
       playerID int,
       side boolean NOT NULL,
       FOREIGN KEY(matchID) REFERENCES match(id),
       FOREIGN KEY(playerID) REFERENCES player(id)
);
