# file contains all methods which deal with fetching log and matches


from sqlalchemy.sql import select, insert, delete, update, desc, join, distinct, Select, between
from sqlalchemy.engine import Engine
from application.auth.account import account
from sqlalchemy.types import DateTime, Date, Time, Text
from application.domain.char import char
from application.domain.match import match
from application.domain.log import log


from application.domain.player import Player
from datetime import date as pydate
import os
from random import choice

def delete_log(self, log_id:int, user_id: int):
    #Check user owns the log they are trying to delete
    sql = self.log.delete().where((self.log.c.id == log_id) & (self.log.c.owner_id == user_id))
    # delete cascades to match and match_player
    with self.engine.connect() as conn:
        conn.execute(sql)
        
def update_char(self, id, char_class, server):
    sql = update(self.char).values(char_class=char_class,
                 server=server).where(self.char.c.id == id)
    with self.engine.connect() as conn:
        conn.execute(sql)


def get_chars(self, user_id):
    j = self.log.join(self.char)
    sql = select([self.char]).select_from(
        j).distinct().where(self.log.c.owner_id == user_id)
    with self.engine.connect() as conn:
        chars = []
        result_set = conn.execute(sql)
        for row in result_set:
            a = char(row[self.char.c.id], row[self.char.c.name],
                     row[self.char.c.char_class], row[self.char.c.server])
            chars.append(a)
    return chars


def get_char_name_by_id(self, char_id: int):
    sql = select([self.char.c.name]).where(self.char.c.id == char_id)
    with self.engine.connect() as conn:
        rs = conn.execute(sql)
        return rs.fetchone()[self.char.c.name]


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


def update_match(self, conn, match: match, log_id: int):

        sql = update(self.match).values(round1=match.round1, round2=match.round2,
                     round3=match.round3, note=match.note) .where((self.match.c.id == match.id))
        conn.execute(sql)

def get_logs(self, user_id, chars=None, date_range=None, servers=None, player_class=None,  only_details=False):
    j = self.log.join(self.char)
    
        
    sql = select([distinct(self.log.c.id),self.log.c.start_date, self.char.c.name, self.log.c.note]).select_from(j).where(self.log.c.owner_id==user_id).order_by(desc(self.log.c.start_date))
    
    # adding where clauses if parameters are given
    if chars:
        sql = sql.where(self.char.c.name.in_(chars))
    if date_range:
        sql = sql.where(between(self.log.c.start_date, date_range[0], date_range[1]) )
    if servers:
        sql = sql.where(self.char.c.server.in_(servers))
    if player_class:
        sql = sql.where(self.char.c.char_class.in_(player_class))
    

    logs=[]
    with self.engine.connect() as conn:
        
        result_set = conn.execute(sql)
        for row in result_set:
            
            log_id=row[self.log.c.id]
            if only_details:
                matches=[]
            else:
                matches = self.get_matches([log_id])
            name = row[self.char.c.name]
            note = row[self.log.c.note]
            logs.append(log(log_id, row[self.log.c.start_date],name, matches = matches, note=note))
        

    return logs

def get_log(self, log_id, owner_id, only_details=False):
        j = self.log.join(self.char)
        # owner_id to make sure user is accessing a log he owns
        sql = select([self.log, self.char.c.name]).select_from(j).where((self.log.c.id == log_id) & (self.log.c.owner_id== owner_id))
        with self.engine.connect() as conn:
            result = conn.execute(sql)
            row = result.fetchone()
            if only_details:
                matches = []
            else:
                matches = self.get_matches([log_id])
            name = row[self.char.c.name]
            note = row[self.log.c.note]
            return log(log_id, row[self.log.c.start_date], name, matches = matches, note=note)

def update_log(self, new_note, owner_id: int, log_id, matches: list, date: str):

    sql = update(self.log).values(note=new_note, start_date=pydate.fromisoformat(
        date)).where((self.log.c.id == log_id) & (self.log.c.owner_id == owner_id))
    
    with self.engine.connect() as conn:
        trans = conn.begin()  # transaction to insure match is not updated unless log is updated
        try:
            result = conn.execute(sql)
            if result.rowcount == 0:  # means user tried to update a log that didn't belong to them
                raise ValueError("user tried to access a log that didn't belong to them")

            result.close()

            # checking that the user hasn't modified the list of match_ids he provided
            allowed_matches = self.get_match_ids([log_id])
            for match in matches:
                if match.id in allowed_matches:
                    self.update_match(conn, match, log_id)
                else:
                    raise ValueError(
                        "match id didn't belong to the log being updated")

            trans.commit()
            print("updated log")
            trans.close()
        except ValueError as e:
            trans.rollback()
            trans.close()
            raise e
        except Exception as e:
            print(e)
            trans.rollback()
            trans.close()
            raise e

def insert_match(self, log_id: int, match: match):
        sql = self.match.insert().values(log_id=log_id, round1=match.round1, round2=match.round2, round3=match.round3, start_time=match.start, end_time = match.end, note=match.note)
        with self.engine.connect() as conn:
            result=conn.execute(sql)
            match_id= result.inserted_primary_key[0]
            # TODO make this with insert in bulk
            for player in match.team:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=1)
                conn.execute(sql)
            for player in match.opponent:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=0)
                conn.execute(sql)
        return match_id 

def get_char_class_by_name(self, names: list, server=None):
    #get_id inserts player if he's not in the database TODO make this insert in bulk
    for player in names:
        self.get_player_id(player)
    sql = select([self.player.c.player_class, self.player.c.name]).where(self.player.c.name.in_(names))
    if server:
        sql = sql.where(self.player.c.server == server)
    results = []
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        for row in result_set:
            results.append( (row[self.player.c.name],row[self.player.c.player_class]) )
        result_set.close()
    return results



def get_match_ids(self, log_ids):
    sql = select([self.match.c.id],self.match.c.log_id.in_(log_ids))
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        matches=[]
        for row in result_set:
            matches.append(row[self.match.c.id])
    return matches
    
def get_team_and_opponents(self, match_id: int):
    j = self.match_player.join(self.player)
    sql = select([self.match_player, self.player.c.name]).select_from(j).where(self.match_player.c.match_id==match_id)
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        team = []
        enemy = []
        for row in result_set:
            if row[self.match_player.c.side]:
                    team.append(row[self.player.c.name])
            else:
                enemy.append(row[self.player.c.name])
    return team, enemy

def update_log_note(self, log_id, new_note, owner_id):
    # owner id to make sure user owns the log he's trying to update
    sql = update(self.log).values(note=new_note).where((self.log.c.id == log_id) & (self.log.c.owner_id == owner_id))
    with self.engine.connect() as conn:
        conn.execute(sql)

def insert_log(self, owner_id: int, matches: list, date: str, player: str): 
    sql = select([self.char.c.id]).where(self.char.c.name == player)
                    
    with self.engine.connect() as conn:
        result=conn.execute(sql)
        row = result.fetchone()
        
        if row is not None:
            char_id=row[self.char.c.id]

        else:
            sql = self.char.insert().values(name = player, owner_id=owner_id)
            result=conn.execute(sql)
            char_id = result.inserted_primary_key[0]
            

        sql = self.log.insert().values(owner_id=owner_id, start_date=pydate.fromisoformat(date), log_file = None, char_id=char_id)

        result=conn.execute(sql)
        log_id = result.inserted_primary_key[0]
    
        for match in matches:
            self.insert_match(log_id, match)


def get_matches(self, log_ids):
    # if other_class:
    #     j = self.match.join(self.match_player).join(self.player)
    #     sql = select([ distinct(self.match.c.id), self.match.c.start_time,self.match.c.note, self.match.c.end_time, self.match.c.round1, self.match.c.round2, self.match.c.round3]).select_from(j).where((self.match.c.log_id.in_(log_ids)) & (self.player.c.player_class.in_(other_class)) )
    #     print(sql)
    # else:
    sql = select([self.match],self.match.c.log_id.in_(log_ids))
    matches= []
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        
        for row in result_set:
            
            team, enemy = self.get_team_and_opponents(row[self.match.c.id])
            matches.append(match(row[self.match.c.start_time],row[self.match.c.end_time], row[self.match.c.round1], row[self.match.c.round2], row[self.match.c.round3], team, enemy, id=row[self.match.c.id], note=row[self.match.c.note]))
    
    return matches
            
