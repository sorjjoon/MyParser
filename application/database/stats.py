
from application import db
from sqlalchemy import text
import os
from typing import List #so we can check param list contains only ints 

#For queries in a more readable format see documentation

def win_pre(log_ids: List[int]):
    
    if len(log_ids)==1:
        ids="("+str(log_ids[0])+")" 
    else:
        ids=str(tuple(log_ids)) #tuple has a string format of what we need, for example (1,2,3)

    if not log_ids:
        return 0
    if os.environ.get("HEROKU"):
    #diffrent versions for postgre and lite (avg(boolean) not supported in postgre (must be cast to int first))
        sql = "SELECT (((SELECT COALESCE(avg(round2::int),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)+(SELECT COALESCE(avg(round3::int),0)*count(round3::int) from match WHERE LOG_ID IN "+ids+"))/(SELECT count(*) FROM Match WHERE LOG_ID IN"+ids+") ) AS 'avg';"
    else:
        sql = "SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") + (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN "+ids+")/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") ) AS 'avg' ; "

    with db.engine.connect() as conn:        
        result=conn.execute(text(sql))
        avg = result.fetchone()[0]
        result.close()
    return avg


def player_count(log_ids: List[int]):
    #match_ids = db.get_match_ids(log_ids)
    if not log_ids:
        return []
    if len(log_ids)==1:
        ids="("+str(log_ids[0])+")" 
    else:
        ids=str(tuple(log_ids))
    if os.environ.get("HEROKU"):
    #Diffrent versions for lite and postgre (postgre true booleans, sqlite 1 and 0)
        sql =""" 
            SELECT COUNT(case match_player.side when true then 1 else null end) as player_side, 
            COUNT(case match_player.side when false then 1 else null end) as player_against,
            SUM(case match_player.side when true then COALESCE(match.round3::int,match.round2 :: int,0) else null end) / cast(COUNT(case match_player.side when true then 1.0 else null end)as decimal) as player_with_win_pre,
            SUM(case match_player.side when false then COALESCE(match.round3::int,match.round2 :: int,0) else null end) / cast(COUNT(case match_player.side when false then 1.0 else null end)as decimal) as player_against_win_pre,
            player.name 
            FROM "match_player"
            JOIN player ON player.id= match_player.player_id
            JOIN match ON match.id = match_player.match_id
            JOIN log ON log.id = match.log_id
            WHERE log.id IN """+ids+""" 
            GROUP BY player.name 
            ORDER BY COUNT(case match_player.side when true then 1 else null end) + COUNT(case match_player.side when false then 1 else null end) DESC;        
            """

    else:
        sql =""" 
        SELECT COUNT(case match_player.side when true then 1 else null end) as player_side, 
        COUNT(case match_player.side when false then 1 else null end) as player_against,
        SUM(case match_player.side when true then COALESCE(match.round3,match.round2 ,0) else null end) / cast(COUNT(case match_player.side when 1 then 1.0 else null end)as float) as player_with_win_pre,
        SUM(case match_player.side when false then COALESCE(match.round3,match.round2 ,0) else null end) / cast(COUNT(case match_player.side when 0 then 1.0 else null end)as float) as player_against_win_pre,
        player.name 
        FROM "match_player"
        JOIN player ON player.id= match_player.player_id
        JOIN match ON match.id = match_player.match_id
        JOIN log ON log.id = match.log_id
        WHERE log.id IN """+ids+""" 
        GROUP BY player.name 
        ORDER BY COUNT(case match_player.side when true then 1 else null end) + COUNT(case match_player.side when false then 1 else null end) DESC;        
        """ 
    results = []
    with db.engine.connect() as conn:        
        result_set=conn.execute(text(sql))
        
        for row in result_set:
            results.append( [row["name"], row["player_side"], row["player_against"],row["player_with_win_pre"],row["player_against_win_pre"]] )
        result_set.close()
    
    return results


    