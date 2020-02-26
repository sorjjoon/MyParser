#all methods admins have access to
from sqlalchemy.sql import text

def list_users(self):
    sql = text("SELECT account.username as name, count(log.id) as lkm FROM account LEFT OUTER JOIN LOG on log.owner_id = account.id GROUP BY account.username;")
    with self.engine.connect() as conn:
        result_set = conn.execute(sql)
        users = []
        for row in result_set:
            users.append((row["name"], row["lkm"]))
        result_set.close()
        return users

