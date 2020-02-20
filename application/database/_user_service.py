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

            
def get_user_roles(self, user_id):
    j = self.account.join(self.role)
    sql = select([self.role.name]).select_from(j).where(self.account.c.id==user_id)
    with self.engine.connect as conn:
        result_set = conn.execute(sql)
        roles = []
        for row in result_set:
            roles.append(row[self.role.name])
        result_set.close()
    return roles

def get_user_by_id(self, user_id: int):
    j = self.account.join(self.role)
    sql = select([self.role.c.name, self.account.c.username]).select_from(j).where(self.account.c.id==user_id)
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        row = result_set.fetchone()
        
        result_set.close()       
        if row is not None:
            return account(user_id,row[self.account.c.username], row[self.role.c.name])
        else:
            return None
        




