
from application import db
from sqlalchemy import text
from typing import List 

def win_pre(log_ids: List[int]):
    #For this query in a more readable format see documentation
    if len(log_ids)==1:
        ids="("+str(log_ids[0])+")" 
    else:
        ids=str(tuple(log_ids)) #tuple has a string format of what we need, for example (1,2,3)
    
    #Can't be injected since the list we are using has only ints, hence why we are usinc concenation (the real reason is sqlite doesn't support passing list as param)
    sql = "SELECT ((SELECT COALESCE(avg(round2),0)*count(round2) from match WHERE LOG_ID IN "+ids+" AND round3 is null)/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") + (SELECT COALESCE(avg(round3),0)*count(round3) from match WHERE LOG_ID IN "+ids+")/(SELECT count(*) FROM Match WHERE LOG_ID IN "+ids+") ) AS 'avg' ; "
    
    with db.engine.connect() as conn:        
        result=conn.execute(text(sql))
        avg = result.fetchone()[0]
        result.close()
    return avg

    