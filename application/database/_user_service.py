from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, LargeBinary, Date, Boolean, DateTime, engine
from sqlalchemy.sql import select, insert, delete, update, desc, join, distinct, Select, between

from application.auth.account import account
from sqlalchemy.types import DateTime, Date, Time, Text


def delete_user(self, user_id):
    sql = self.account.delete().where(self.account.c.id == user_id)
    with self.engine.connect() as conn:
        conn.execute(sql) #delete cascades

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
        




