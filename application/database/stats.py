
from application import db
from sqlalchemy import text
from typing import List #so we can check param list contains only ints 

def win_pre(log_ids: List[int]):
    #For this query in a more readable format see documentation
    if len(log_ids)==1:
        ids="("+str(log_ids[0])+")" 
    else:
        ids=str(tuple(log_ids)) #tuple has a string format of what we need, for example (1,2,3)
    
    #Can't be injected since the list we are using has only ints, hence why we are usinc concenation (the real reason is sqlite doesn't support passing list as param)
    sql = "SELECT ((SELECT COALESCE(avg(round2::int),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") + (SELECT COALESCE(avg(round3::int),0)*count(round3) from match WHERE LOG_ID IN "+ids+")/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") ) AS 'avg' ; "
    
    with db.engine.connect() as conn:        
        result=conn.execute(text(sql))
        avg = result.fetchone()[0]
        result.close()
    return avg


def player_count(log_ids: List[int]):
    match_ids = db.get_match_ids(log_ids)
    if len(match_ids)==1:
        ids="("+str(match_ids[0])+")" 
    else:
        ids=str(tuple(match_ids))

    #Can't be injected since the list we are using has only ints, hence why we are usinc concenation (the real reason is sqlite doesn't support passing list as param)
    sql = """SELECT COUNT(case match_player.side when 1 then 1 else null end) as player_side, COUNT(case match_player.side when 0 then 1 else null end) as player_against, player.name FROM match_player
            JOIN player ON player.id = match_player.player_id
            WHERE match_player.match_id IN """+ids+" GROUP BY player_name ORDER BY player_side DESC;" 
    results = []
    with db.engine.connect() as conn:        
        result_set=conn.execute(text(sql))
        for row in result_set:
            results.append( (row["name"], row["player_side"], row["player_against"]) )


        result_set.close()
    
    return results


    