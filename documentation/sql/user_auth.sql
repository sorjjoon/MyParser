--def get_user(self, username: str, password: str):
--first the password is hased using the function hash_password (see line ), and we try to find a username/password combination in the database 
SELECT * FROM account WHERE username = 'something' AND password = 'asdlkjfdsfnsdlfndlsfndssdlfkn'     
--if no match is found, None is returned

--def get_role_id(self, role):
SELECT id FROM role WHERE name = 'ADMIN'

--def insert_user(self, username: str, password: str, role='USER'):
--salt is generated in a seperate function (so it can be swapped in the future if wanted)
--after the new salt + password combo is hashed, we fetch the role_id for role we are inserting with get_role_id (see line 7)
INSERT INTO account (username, password, salt, role_id) VALUES ('something', 'pasdjaodmkpasdkadoq2asdasdasdasdasda012', 'dasolrh238042jioiensdlfjpolnfdlsknf', 1)

--def hash_password(self, password, username=None, user_id=None):
--fetches a salt for a given username or user and hashes the given password accordingly
SELECT salt FROM account WHERE id = 2;
-- or if name is given
SELECT salt FROM account WHERE username = 'something'

--def update_password(self, user_id: int, new_password: str):
--after hashing the new password with the fucntion hash_password (see line 14)
UPDATE account SET password = 'asldknjalsdjelq2l2k1nl' WHERE id = 2;
