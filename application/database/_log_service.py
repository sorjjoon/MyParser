import os
from datetime import date as pydate
from random import choice

from sqlalchemy.sql import (Select, between, delete, desc, distinct, insert,
                            join, select, update)

from application.auth.account import account
from application.domain.char import char
from application.domain.log import log
from application.domain.match import match
from application.domain.player import Player


def get_logs(self, user_id, chars=None, date_range=None, servers=None, player_class=None,  only_details=False):
    
    join_clause = self.log.join(self.char)
        
    sql = select([distinct(self.log.c.id),self.log.c.start_date, self.char.c.name, self.log.c.note]).select_from(join_clause)

    sql = sql.where(self.log.c.owner_id==user_id)
    sql = sql.order_by(desc(self.log.c.start_date))

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

def get_single_log(self, log_id, owner_id, only_details=False):
        join_clause = self.log.join(self.char)
        # owner_id to make sure user is accessing a log he owns
        sql = select([self.log, self.char.c.name]).select_from(join_clause)
        sq = sql.where((self.log.c.id == log_id) & (self.log.c.owner_id== owner_id))

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

def delete_log(self, log_id:int, user_id: int):
    #Check user owns the log they are trying to delete
    sql = self.log.delete().where((self.log.c.id == log_id) & (self.log.c.owner_id == user_id))
    # delete cascades to match and match_player
    with self.engine.connect() as conn:
        conn.execute(sql)

def update_log(self, new_note, owner_id: int, log_id, new_matches: list, date: str):

    sql = update(self.log).values(note=new_note, start_date=pydate.fromisoformat(
        date)).where((self.log.c.id == log_id) & (self.log.c.owner_id == owner_id))
    
    with self.engine.connect() as conn:
        trans = conn.begin()  # transaction to insure match is not updated unless log is updated
        try:
            result = conn.execute(sql)
            if result.rowcount == 0:  # means user tried to update a log that didn't belong to them (or doesn't exsist)
                raise ValueError("user tried to access a log that didn't belong to them")

            result.close()

            # checking that the user hasn't modified the list of match_ids he provided  (allowed matches contains only matches belonging to the match the user tries to modify)
            allowed_matches = self.get_match_ids([log_id])
            for match in new_matches:
                if match.id in allowed_matches:
                    self.update_match(conn, match, log_id)
                else:
                    raise ValueError(
                        "match id didn't belong to the log being updated")

            trans.commit()
            print("updated log "+str(log_id))
            trans.close()
        except ValueError as e:
            trans.rollback()
            trans.close()
            raise e
        except Exception as e:
            print("unexpected error")
            print(e)
            trans.rollback()
            trans.close()
            raise e

def update_log_note(self, log_id, new_note, owner_id):
    # owner id to make sure user owns the log he's trying to update
    sql = update(self.log).values(note=new_note).where((self.log.c.id == log_id) & (self.log.c.owner_id == owner_id))
    with self.engine.connect() as conn:
        conn.execute(sql)

def insert_log(self, owner_id: int, matches: list, date: str, char: str, note=None): 
    sql = select([self.char.c.id]).where((self.char.c.name == char) & (self.char.c.owner_id == owner_id))
                    
    with self.engine.connect() as conn:
        result=conn.execute(sql)
        row = result.fetchone()
        
        if row is not None:
            char_id=row[self.char.c.id]

        else:
            sql = self.char.insert().values(name = char, owner_id=owner_id)
            result=conn.execute(sql)
            char_id = result.inserted_primary_key[0]
            

        sql = self.log.insert().values(owner_id=owner_id, start_date=pydate.fromisoformat(date), char_id=char_id, note=note)

        result=conn.execute(sql)
        log_id = result.inserted_primary_key[0]
    
        for match in matches:
            self.insert_match(log_id, match)
