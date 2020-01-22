CREATE TABLE User (
       username varchar(20),
       password varchar(30),
       id int,
       PRIMARY KEY(id)
);



CREATE TABLE Log (
       id int,
       ownerID int,
       date date,
       PRIMARY KEY(id),
       FOREIGN KEY(ownerID) REFERENCES User(id)
);

CREATE TABLE Player (
       name varchar(20),
       id int,
       PRIMARY KEY(id)
);

CREATE TABLE Match (
       id int,
       round1 boolean,
       round2 boolean,
       round3 boolean,
       timestamp time,
       PRIMARY KEY(id)
);

CREATE TABLE match_player (
       matchID int,
       playerID int,
       FOREIGN KEY(matchID) REFERENCES match(id),
       FOREIGN KEY(playerID) REFERENCES player(id)
);
       
