import os
from datetime import date as pydate
from random import choice

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        LargeBinary, MetaData, String, Table, engine, UniqueConstraint)
from sqlalchemy.engine import Engine
from sqlalchemy.sql import (Select, between, delete, desc, distinct, insert,
                            join, select, update)
from sqlalchemy.types import Date, DateTime, Text, Time, VARBINARY
from sqlalchemy.dialects.postgresql import BYTEA
from application.auth.account import account
from application.domain.char import char
from application.domain.log import log
from application.domain.match import match
from application.domain.player import Player
import os

#TODO close all result_sets
class data:
    def __init__(self, used_engine: engine):
        if not os.environ.get("HEROKU"):
            #sqlite doesn't enforce foreign keys by default, turning them on to enforce cascade
            def _fk_pragma_on_connect(dbapi_con, con_record):
                dbapi_con.execute('pragma foreign_keys=ON')

            from sqlalchemy import event
            event.listen(used_engine, 'connect', _fk_pragma_on_connect)

        metadata = MetaData()

        self.role = Table("role", metadata,
        Column("id",Integer, primary_key=True),
        Column("name",String(20)),
        UniqueConstraint('name', name='role_unique' #TODO remove this (unnecessary index for a small table)
        ))

        self.account = Table('account', metadata,
        Column("id",Integer, primary_key=True),
        Column("role_id",Integer, ForeignKey("role.id", onupdate="CASCADE")),
        Column("username",String(150), nullable=False),
        Column("salt", String(144), nullable=False),
        Column("password",String(150), nullable=False),
        UniqueConstraint('username', name='username_unique')
        )
    
     
        self.log = Table('log', metadata,
        Column("id",Integer, primary_key=True ),
        Column("note",Text),
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
        Column("id",Integer, primary_key=True),
        UniqueConstraint('name', 'server', name='player_server_unique')
        )

        self.engine=used_engine
        metadata.create_all(used_engine) #checks if table exsists first

        #insert 1 admin user, and roles "USER" and "ADMIN to the database (if they don't exsist)"
        
        with self.engine.connect() as conn:
            sql = self.role.insert().values(name="USER", id=1)

            #catches unqiue contraint fail
            try:
                
                conn.execute(sql)
                print("user role inserted")
            except:
                pass
            sql = self.role.insert().values(name="ADMIN", id=2)
            try:
                conn.execute(sql)
                print("admin role inserted")

            except:
                pass

    #just importing everything in this module
    from ._domain_service import update_char, update_log, update_log_note, update_match, get_char_name_by_id, get_char_class_by_name, get_chars, get_log, get_logs, get_match_ids, get_matches, get_player_id, get_team_and_opponents, delete_log, insert_match, insert_log
    from ._user_service import delete_user, get_user_by_id, check_user, get_user_roles
    from ._user_auth import get_user, hash_password, insert_user, update_password, get_role_id
    from ._admin import list_users
    from ._stats import win_pre, player_count
    
