# file contains all methods which deal with fetching log and matches
from datetime import date as pydate
from random import choice

from sqlalchemy.sql import (Select, between, delete, desc, distinct, insert,
                            join, select, update)

from application.auth.account import account
from application.domain.char import char
from application.domain.log import log
from application.domain.match import match
from application.domain.player import Player

#for all queries in a readable format, and explanation for diffrent optional params, see documentation

        



def update_match(self, conn, match: match, log_id: int):

        sql = update(self.match).values(round1=match.round1, round2=match.round2,
                     round3=match.round3, note=match.note) .where((self.match.c.id == match.id))
        conn.execute(sql)



def insert_match(self, log_id: int, match: match):
        sql = self.match.insert().values(
        log_id=log_id, 
        round1=match.round1, 
        round2=match.round2, 
        round3=match.round3, 
        start_time=match.start, 
        end_time = match.end, 
        note=match.note)

        with self.engine.connect() as conn:
            result=conn.execute(sql)
            match_id= result.inserted_primary_key[0]
            # TODO make this with insert in bulk
            for player in match.team:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, owner_side=1)
                conn.execute(sql)
            for player in match.opponent:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, owner_side=0)
                conn.execute(sql)
        return match_id 





def get_match_ids(self, log_ids):
    sql = select([self.match.c.id],self.match.c.log_id.in_(log_ids))
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        matches=[]
        for row in result_set:
            matches.append(row[self.match.c.id])
    return matches
    
    #conn parameter in case we don't want to open a new connection (get_matches method already has a connection open when calling this)
def get_team_and_opponents(self, match_id: int, conn=None):
    join_clause = self.match_player.join(self.player)
    sql = select([self.match_player, self.player.c.name]).select_from(join_clause).where(self.match_player.c.match_id==match_id)
    if conn is None:
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            team = []
            enemy = []
            for row in result_set:
                if row[self.match_player.c.owner_side]:
                        team.append(row[self.player.c.name])
                else:
                    enemy.append(row[self.player.c.name])
    else:
        result_set = conn.execute(sql)
        team = []
        enemy = []
        for row in result_set:
            if row[self.match_player.c.owner_side]:
                    team.append(row[self.player.c.name])
            else:
                enemy.append(row[self.player.c.name])

    return team, enemy




def get_matches(self, log_ids):
  
    sql = select([self.match],self.match.c.log_id.in_(log_ids))
    matches= []
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        
        for row in result_set:
            
            team, enemy = self.get_team_and_opponents(row[self.match.c.id], conn=conn) #TODO fetch this in bulk
            new_match = match(row[self.match.c.start_time],row[self.match.c.end_time], row[self.match.c.round1], row[self.match.c.round2], row[self.match.c.round3], team, enemy, id=row[self.match.c.id], note=row[self.match.c.note])
            matches.append(new_match)
    
    return matches



def get_player_id(self, player_name: str):
        sql = select([self.player.c.id]).where(self.player.c.name == player_name)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            result_set.close()
            if row is None:
                # picking a random class for sample data
                player_class = choice(["Mercenary", "Powertech", "Juggernaut",
                                      "Marauder", "Assassin", "Sorcerer", "Operative", "Sniper"])
                sql = self.player.insert().values(name=player_name, player_class=player_class)
                result = conn.execute(sql)
                return result.inserted_primary_key[0]
            else:
                return row[self.player.c.id]
