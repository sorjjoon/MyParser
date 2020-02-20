#all methods admins have access to
from sqlalchemy.sql import select, insert, delete, update, desc, join, distinct, Select, between

def list_users(self):
    sql = select([self.account.c.username])
    with self.engine.connect() as conn:
        rs = conn.execute(sql)
        users = []
        for row in rs:
            users.append(row[self.account.c.username])
        rs.close()
        return users

