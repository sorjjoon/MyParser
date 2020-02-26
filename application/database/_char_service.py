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


def update_char(self, id, char_class, server):
    sql = update(self.char).values(char_class=char_class,
                 server=server).where(self.char.c.id == id)
    with self.engine.connect() as conn:
        conn.execute(sql)


def get_chars(self, user_id):
    join_clause = self.log.join(self.char)
    sql = select([self.char]).select_from(join_clause).distinct().where(self.log.c.owner_id == user_id)
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
        result_set = conn.execute(sql)
        return result_set.fetchone()[self.char.c.name]


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
