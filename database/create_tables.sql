CREATE TABLE IF NOT EXISTS User (
       username varchar(20) NOT NULL,
       password varchar(30) NOT NULL,
       id int NOT NULL,
       PRIMARY KEY(id)
);



CREATE TABLE IF NOT EXISTS Log (
       id int NOT NULL,
       ownerID int NOT NULL,
       date date NOT NULL,
       PRIMARY KEY(id),
       FOREIGN KEY(ownerID) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Player (
       name varchar(20) NOT NULL,
       id int NOT NULL,
       PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Match (
       id int NOT NULL,
       round1 boolean,
       round2 boolean,
       round3 boolean,
       timestamp time,
       PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS match_player (
       matchID int NOT NULL,
       playerID int NOT NULL,
       side boolean NOT NULL,
       FOREIGN KEY(matchID) REFERENCES match(id),
       FOREIGN KEY(playerID) REFERENCES player(id)
);
       
