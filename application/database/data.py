from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, LargeBinary, Date, Boolean, DateTime, engine
from sqlalchemy.sql import select, insert, delete, update, desc, join, distinct, Select, between
from sqlalchemy.engine import Engine
from application.auth.account import account
from sqlalchemy.types import DateTime, Date, Time, Text
from application.domain.domain import match, log, char
from application.domain.player import Player
from datetime import date as pydate
import os
from random import choice


class data:
    def __init__(self, used_engine: engine):
        if not os.environ.get("HEROKU"):
            #sqlite doesn't enforce foreign keys by default, turning them on to enforce cascade
            def _fk_pragma_on_connect(dbapi_con, con_record):
                dbapi_con.execute('pragma foreign_keys=ON')

            from sqlalchemy import event
            event.listen(used_engine, 'connect', _fk_pragma_on_connect)

        metadata = MetaData()
        self.account = Table('account', metadata,
        Column("id",Integer, primary_key=True),
        Column("username",String(150), nullable=False),
        Column("password",String(150), nullable=False))
        
        self.log = Table('log', metadata,
        Column("id",Integer, primary_key=True ),
        Column("owner_id",Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False),
        Column("log_file",LargeBinary),
        Column("char_id",Integer, ForeignKey("char.id", onupdate="CASCADE")),
        Column("start_date",Date))


        self.char = Table("char", metadata,
        Column("id",Integer, primary_key=True ),
        Column("name", String(30)),
        Column("server", String(30)),
        Column("owner_id",Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False),
        Column("char_class", String(30)))

        self.match_player = Table('match_player', metadata,
        Column("player_id",Integer, ForeignKey("player.id", onupdate="CASCADE"), primary_key=True),
        Column("match_id",Integer, ForeignKey("match.id", ondelete="CASCADE"), primary_key=True),
        Column("side",Boolean, nullable = False))

        self.match = Table('match', metadata,
        Column("id",Integer, primary_key=True),
        Column("round1",Boolean, nullable=False),
        Column("round2",Boolean, nullable= False),
        Column("round3",Boolean, default= None),
        Column("log_id", Integer, ForeignKey("log.id", ondelete="CASCADE")),
        Column("start_time", Time),
        Column("note", Text),
        Column("end_time", Time))
        
        self.player = Table('player', metadata,    
        Column("name",String(30), nullable = False),
        Column("player_class",String(30)),
        Column("server",String(30)),    
        Column("id",Integer, primary_key=True))

        self.engine=used_engine
        metadata.create_all(used_engine) #checks if table exsists first
    

    def match_update_note(self, match_id, new_note):
        sql = update(self.match).values(note=new_note).where(self.match.c.id==match_id)
        with self.engine.connect() as conn:
            conn.execute(sql)

    def update_char(self, id, char_class, server):
        sql = update(self.char).values(char_class=char_class, server=server).where(self.char.c.id==id) 
        with self.engine.connect() as conn:
            conn.execute(sql)

    def get_char_name_by_id(self, char_id: int):
        sql = select([self.char.c.name]).where(self.char.c.id == char_id)
        with self.engine.connect() as conn:
            rs = conn.execute(sql)
            return rs.fetchone()[self.char.c.name]
        

    def delete_user(self, user_id):
        sql = self.account.delete().where(self.account.c.id == user_id)
        with self.engine.connect() as conn:
            conn.execute(sql) #delete cascades

    def delete_log(self, log_id:int, user_id: int):
        #Check user owns the log they are trying to delete
        sql = self.log.delete().where((self.log.c.id == log_id) & (self.log.c.owner_id == user_id))
        # delete cascades to match and match_player
        with self.engine.connect() as conn:
            conn.execute(sql)

    def insert_user(self, username: str, password: str):
        print("Adding new user "+username)
        sql = self.account.insert().values(username=username, password=password)
        with self.engine.connect() as conn:
            conn.execute(sql)
                

    def get_user_by_id(self, user_id: int):
        sql = select([self.account]).where(self.account.c.id==user_id)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            
            result_set.close()       
            if row is not None:
                return account(row[self.account.c.id],row[self.account.c.username], row[self.account.c.password])
            else:
                return None
            
    def get_chars(self, user_id):
        j = self.log.join(self.char)
        sql = select([self.char]).select_from(j).distinct().where(self.log.c.owner_id==user_id)
        with self.engine.connect() as conn:
            chars = []
            result_set = conn.execute(sql)
            for row in result_set:
                a= char( row[self.char.c.id], row[self.char.c.name], row[self.char.c.char_class], row[self.char.c.server] )
                chars.append(a)
        return chars


    def update_password(self, user_id: int, new_password: str):
        print("fetching password for "+str(user_id))
        sql = update(self.account).values(password=new_password).where(self.account.c.id==user_id)
        with self.engine.connect() as conn:
            conn.execute(sql)
    
    def get_user(self, username: str, password: str):        
        sql = select([self.account]).where(self.account.c.username==username).where(self.account.c.password==password)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            result_set.close()
            if row is not None:
                print("Login for "+username+" success")
                return account(row[self.account.c.id],row[self.account.c.username], row[self.account.c.password])
            else:
                print("Login for "+username+" failed")
                return None


    def get_logs(self, user_id, chars=None, date_range=None, servers=None, player_class=None, enemy_class = None):
        j = self.log.join(self.char)
            
        sql = select([self.log.c.id,self.log.c.start_date, self.char.c.name]).select_from(j).where(self.log.c.owner_id==user_id).order_by(desc(self.log.c.start_date))
        
        #adding where clauses if parameters are given
        if chars:
            sql = sql.where(self.char.c.name.in_(chars))
        if date_range:
            sql = sql.where(between(self.log.c.start_date, date_range[0], date_range[1]) )
        if servers:
            sql = sql.where(self.char.c.server.in_(servers))
        if player_class:
            sql = sql.where(self.char.c.char_class.in_(player_class))
        if enemy_class:
            pass

        logs=[]
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            for row in result_set:
               
                log_id=row[self.log.c.id]
                matches = self.get_matches([log_id])
                name = row[self.char.c.name]
                logs.append(log(log_id, row[self.log.c.start_date],name, matches = matches))
            

        return logs


    def check_user(self, username):
        sql = select([self.account]).where(self.account.c.username==username)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            result_set.close()
            if row is None:
                return True
            else:
                return False

    def get_player_id(self, player_name: str):
        sql = select([self.player]).where(self.player.c.name==player_name)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            result_set.close()
            if row is None:
                player_class = choice(["Mercenary","Powertech", "Juggernaut", "Marauder","Assassin","Sorcerer","Operative","Sniper"])
                sql = self.player.insert().values(name=player_name)
                result = conn.execute(sql)
                return result.inserted_primary_key[0]
            else:
                return row[self.player.c.id]
                

    def __insert_match(self, log_id: int, match: match):
        sql = self.match.insert().values(log_id=log_id, round1=match.round1, round2=match.round2, round3=match.round3, start_time=match.start, end_time = match.end, note=match.note)
        with self.engine.connect() as conn:
            result=conn.execute(sql)
            match_id= result.inserted_primary_key[0]
            #TODO make this with insert in bulk
            for player in match.team:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=1)
                conn.execute(sql)
            for player in match.opponent:
                player_id = self.get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=0)
                conn.execute(sql)
        return match_id 

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
                self.__insert_match(log_id, match)

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

    def get_matches(self, log_ids):
        #TODO combine these 2 queries
        sql = select([self.match],self.match.c.log_id.in_(log_ids))
        matches= []
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            
            for row in result_set:
                team, enemy = self.get_team_and_opponents(row[self.match.c.id])
                matches.append(match(row[self.match.c.start_time],row[self.match.c.end_time], row[self.match.c.round1], row[self.match.c.round2], row[self.match.c.round3], team, enemy, note=row[self.match.c.note]))
        
        return matches
                

    

    
        
        

        


        
