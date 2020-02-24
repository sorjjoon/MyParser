#all methods admins have access to
from sqlalchemy.sql import select, insert, delete, update, desc, join, distinct, Select, between, text

def list_users(self):
    sql = text("SELECT account.username as name, count(log.owner_id) as lkm FROM log JOIN account ON log.owner_id = account.id GROUP BY account.id")
    with self.engine.connect() as conn:
        rs = conn.execute(sql)
        users = []
        for row in rs:
            users.append((row["name"], row["lkm"]))
        rs.close()
        return users

