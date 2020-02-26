--All quries have some sample data in them (all ids are 2)

--delete_log(self, log_id:int, user_id: int):
DELETE FROM LOG 
WHERE log.id = 2 AND log.owner_id = 2;

--update_char(self, id, char_class, server):
UPDATE char SET player_class='Operative', server='Darth Malgus' 
WHERE id = 2;

--get_chars(self, user_id):
SELECT *
FROM char
    JOIN log ON log.char_id = char.id
WHERE log.owner_id = 2;


-- get_char_name_by_id(self, char_id: int):
SELECT char.name
FROM char
WHERE char.id = 2;


-- get_player_id(self, player_name: str): insert is only applied, if the player is not found
SELECT player.id
FROM player
WHERE player.name = '@something'

INSERT INTO player
    (name, player_class)
VALUES
    ('@something', 'Operative')


-- def update_match(self, conn, match: match, log_id: int):
UPDATE match SET round1 = TRUE, round2 = TRUE, round3 = NULL, note ='something' 
WHERE id = 2


-- get_logs(self, user_id, chars=None, date_range=None, servers=None, player_class=None,  only_details=False):
SELECT DISTINCT log.id, log.start_date, log.note, char.name
FROM log
    JOIN char ON log.char_id = char.id
WHERE log.owner_id = 2
ORDER BY log.start_date DESC;
-- This is the query that's done when all logs have to be returned. In addition this query can be added more WHERE clauses if we want to limit the results (optional params in function) 
-- WHERE clases are added as simple AND clauses after log.owner_id = 2, like so
SELECT DISTINCT log.id, log.start_date, log.note, char.name
FROM log
    JOIN char ON log.char_id = char.id
WHERE log.owner_id = 2 AND char.name IN ('@something', '@other')
ORDER BY log.start_date DESC;
--These AND clauses are added as many as needed, here an example with all possible clauses added
SELECT DISTINCT log.id, log.start_date, log.note, char.name
FROM log
    JOIN char ON log.char_id = char.id
WHERE log.owner_id = 2
    AND char.name IN ('@something', '@other')
    AND log.start_date BETWEEN '2019-07-01' AND '2019-07-31'
    AND char.server IN ('Darth Malgus', 'Satele Shan')
    AND char.char_class IN ('Operative', 'Sniper')
ORDER BY log.start_date DESC;

--Note naming, returns only a single log
--def get_single_log(self, log_id, owner_id, only_details=False): only_details limits if match data is added to a log object 
--log details gotten with,
SELECT *
FROM log JOIN char ON char.id = log.char_id
WHERE log.id = 2 AND log.owner_id = 2;
--if only_details is true, get_matches (see line 128) function is used to make a list of all matches belonging to a log (otherwise an empty list is used)


--def update_log(self, new_note, owner_id: int, log_id, matches: list, date: str): 
--the following queries are done with a transaction, to insure match and log are updated only if no problems are encountered
--Most importantly, if the user has modified the list of logs / matches he provided he could attempt to modify a log/match he doesn't own 
--in this case the transaction is rolled back
UPDATE log SET note = 'something', start_date = '2019-07-01' WHERE id = 2 AND log.owner_id = 2;

-- The list of match ids belonging to the match is fetched with the function get_match_ids (see line 91), and each match_id is verified to be contained in the list
-- if any match_id isn't found in the list, the transaction is rolled back
-- match updating is done with the function update_match (see line 35)



--def insert_match(self, log_id: int, match: match):
INSERT INTO match
    (log_id, round1, round2, round3, start_time, end_time, note)
VALUES(2, false, true, true, '10:05:06.789', '10:20:05.123', 'something')


--def get_match_ids(self, log_ids):
SELECT id
FROM match
WHERE log_id IN (1,2,3);



-- def get_team_and_opponents(self, match_id: int, conn=None):
-- conn parameter in case we don't want to open a new connection (get_matches function already has a connection open when calling this)
SELECT match_player.player_id, match_player.match_id, match_player.owner_side, player.name
FROM match_player JOIN player ON player.id = match_player.player_id
WHERE match.match_id = 2
--side parameters tells if a player was playing against/with player and results are grouped by this


--def update_log_note(self, log_id, new_note, owner_id):
UPDATE log SET note = 'something' WHERE id = 2 AND owner_id = 2;


-- def insert_log(self, owner_id: int, matches: list, date: str, player: str): 
-- first find out if the char is already in the database
SELECT char.id
FROM char
WHERE name = '@something' AND owner_id = 2;
--if not found, insert a new char
INSERT INTO char
    (name, owner_id)
VALUES
    ('@something', 2);
--after everything, a new log is inserted the char.id of the foung/inserted char
INSERT INTO log
    (owner_id, start_date, char_id)
VALUES
    (2, '2019-07-01', 2);
--matches are insrted using the function insert_match (see line 85)


--def get_matches(self, log_ids):
SELECT *
FROM match
WHERE log_id IN (1,2,3,4);
--the team/opponents of each match is done using the function get_team_and_opponents  (see line 98)

            
