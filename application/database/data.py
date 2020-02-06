from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, LargeBinary, Date, Boolean, DateTime, engine
from sqlalchemy.sql import select, insert, delete, update, desc
from application.auth.account import account
from sqlalchemy.types import DateTime, Date, Time
from application.domain.domain import match, log
from datetime import date as pydate

class data:
    def __init__(self, used_engine: engine):
        #Creating tables
        
        metadata = MetaData()
        self.account = Table('Account', metadata,
        Column("id",Integer, primary_key=True),
        Column("username",String(150), nullable=False),
        Column("password",String(150), nullable=False))
        
        self.log = Table('Log', metadata,
        Column("id",Integer, primary_key=True),
        Column("owner_id",Integer, ForeignKey("Account.id"), nullable=False),
        Column("log_file",LargeBinary),
        Column("start_date",Date))

        self.match_player = Table('match_player', metadata,
        Column("player_id",Integer, ForeignKey("Player.id"), primary_key=True),
        Column("match_id",Integer, ForeignKey("Match.id"), primary_key=True),
        Column("side",Boolean, nullable = False))

        self.match = Table('Match', metadata,
        Column("id",Integer, primary_key=True),
        Column("round1",Boolean),
        Column("round2",Boolean),
        Column("round3",Boolean, default= None),
        Column("log_id",Integer, ForeignKey("Log.id")),
        Column("start_time", Time),
        Column("end_time", Time))
        
        self.player = Table('Player', metadata,    
        Column("name",String(30), nullable = False),
        Column("id",Integer, primary_key=True))
        self.engine=used_engine
        
        metadata.create_all(used_engine)


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


    def get_logs(self, user_id):
        
        sql = select([self.log.c.id,self.log.c.start_date]).where(self.log.c.owner_id==user_id).order_by(desc(self.log.c.start_date))
        logs=[]
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            for row in result_set:
               
                log_id=row[self.log.c.id]
                matches = self.get_matches([log_id])
                logs.append(log(log_id, row[self.log.c.start_date], matches = matches))
            

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

    def get_player_id(self, player_name):
        sql = select([self.player]).where(self.player.c.name==player_name)
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            row = result_set.fetchone()
            result_set.close()
            if row is None:
                sql = self.player.insert().values(name=player_name)
                result = conn.execute(sql)
                return result.inserted_primary_key[0]
            else:
                return row[self.player.c.id]
                

    def __insert_match(self, log_id: int, match: match):
        sql = self.match.insert().values(log_id=log_id, round1=match.round1, round2=match.round2, round3=match.round3, start_time=match.start, end_time = match.end)
        with self.engine.connect() as conn:
            result=conn.execute(sql)
            match_id= result.inserted_primary_key[0]
            #TODO make this with insert in bulk
            for player in match.team:
                player_id = get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=1)
                conn.execute(sql)
            for player in match.opponent:
                player_id = get_player_id(player)
                sql = self.match_player.insert().values(player_id=player_id,match_id = match_id, side=0)
                conn.execute(sql)
        return match_id 

    def insert_log(self, owner_id: int, matches: list, date: str): 
                      
        sql = self.log.insert().values(owner_id=owner_id, start_date=pydate.fromisoformat(date), log_file = None)
        with self.engine.connect() as conn:
            result=conn.execute(sql) 
            log_id = result.inserted_primary_key[0]
        
            for match in matches:
                self.__insert_match(log_id, match)

    def get_matches(self, log_ids):
        sql = select([self.match],self.match.c.log_id.in_(log_ids))
        matches= []
        with self.engine.connect() as conn:
            result_set = conn.execute(sql)
            print
            for row in result_set:
                print(row)
                matches.append(match(row[elf.match.c.start_time],row[self.match.c.end_time], row[self.match.c.round1], row[self.match.c.round2], row[self.match.c.round3], [], []))
        
        return matches
                

    

    
        
        

        


        
