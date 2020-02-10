
from application import db
from sqlalchemy import text
import os
from typing import List #so we can check param list contains only ints 

#For this queries in a more readable format see documentation

def win_pre(log_ids: List[int]):
    
    if len(log_ids)==1:
        ids="("+str(log_ids[0])+")" 
    else:
        ids=str(tuple(log_ids)) #tuple has a string format of what we need, for example (1,2,3)

    if not log_ids:
        return 0
    if os.environ.get("HEROKU"):
    #diffrent versions for postgre and lite (avg(boolean) not supported in postgre (must be cast to int first))
        sql = "SELECT (((SELECT COALESCE(avg(round2::int),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)+(SELECT COALESCE(avg(round3::int),0)*count(round3::int) from match WHERE LOG_ID IN "+ids+"))/(SELECT count(*) FROM Match WHERE LOG_ID IN"+ids+") ) AS "avg";"
        sql = "SELECT ((SELECT COALESCE(avg(round2::int),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") + (SELECT COALESCE(avg(round3::int),0)*count(round3) from match WHERE LOG_ID IN "+ids+")/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") ) AS avg ; "
    else:
        sql = "SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") + (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN "+ids+")/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") ) AS 'avg' ; "

    with db.engine.connect() as conn:        
        result=conn.execute(text(sql))
        avg = result.fetchone()[0]
        result.close()
    return avg


def player_count(log_ids: List[int]):
    match_ids = db.get_match_ids(log_ids)
    if not match_ids:
        return []
    if len(match_ids)==1:
        ids="("+str(match_ids[0])+")" 
    else:
        ids=str(tuple(match_ids))
    if os.environ.get("HEROKU"):
    #Diffrent versions for lite and postgre (postgre true booleans, sqlite 1 and 0)
        sql = """SELECT COUNT(case match_player.side when true then 1 else null end) as player_side, COUNT(case match_player.side when false then 1 else null end) as player_against, player.name FROM "match_player"
                    JOIN player ON player.id= match_player.player_id
                    WHERE match_player.match_id IN """+ids+" GROUP BY player.name ORDER BY COUNT(case match_player.side when true then 1 else null end) + COUNT(case match_player.side when false then 1 else null end);" 
    else:
        sql = """SELECT COUNT(case match_player.side when 1 then 1 else null end) as player_side, COUNT(case match_player.side when 0 then 1 else null end) as player_against, player.name FROM match_player
            JOIN player ON player.id = match_player.player_id
            WHERE match_player.match_id IN """+ids+" GROUP BY player_id ORDER BY (player_side+player_against) DESC;" 
 
    results = []
    with db.engine.connect() as conn:        
        result_set=conn.execute(text(sql))
        for row in result_set:
            results.append( (row["name"], row["player_side"], row["player_against"]) )


        result_set.close()
    
    return results


    