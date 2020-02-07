Table creation

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


queries (the IN clauses have example data in them)

 SELECT (
        (SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)
        /
        (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))
         + 
         (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))
         /
         (SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) 
         
         ) AS "avg";

 
(same but in a single line)     
SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN(1,2) AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2))+ (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN(1,2))/(SELECT count(*) FROM Match WHERE LOG_ID IN(1,2)) ) AS "avg";



Times user has played with other players:

SELECT COUNT(case match_player.side when true then 1 else null end) as player_side, COUNT(case match_player.side when false then 1 else null end) as player_against, player.name FROM "match_player"
JOIN player ON player.id= match_player.player_id
WHERE match_player.match_id IN (1, 125) GROUP BY player.name ORDER BY player_side;