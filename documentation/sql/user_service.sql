--def delete_user(self, user_id):
--note, delete cascades to log/match
DELETE FROM account WHERE id = 2;

--def check_user(self, username):
--check if username is taken
SELECT id
FROM account
WHERE username = 'something';

--def get_user_by_id(self, user_id: int): get user name/role
SELECT role.name, account.username
FROM account JOIN role ON role_id = acccount.role_id
WHERE account.id =2;

