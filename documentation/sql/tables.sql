
CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(20), 
	PRIMARY KEY (id), 
	CONSTRAINT role_unique UNIQUE (name)
)

CREATE TABLE player (
	name VARCHAR(30) NOT NULL, 
	player_class VARCHAR(30), 
	server VARCHAR(30), 
	id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT player_server_unique UNIQUE (name, server)
)

CREATE TABLE account (
	id INTEGER NOT NULL, 
	role_id INTEGER, 
	username VARCHAR(150) NOT NULL, 
	salt VARCHAR(144) NOT NULL, 
	password VARCHAR(150) NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT username_unique UNIQUE (username), 
	FOREIGN KEY(role_id) REFERENCES role (id) ON UPDATE CASCADE
)


CREATE TABLE char (
	id INTEGER NOT NULL, 
	name VARCHAR(30), 
	server VARCHAR(30), 
	owner_id INTEGER NOT NULL, 
	char_class VARCHAR(30), 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES account (id) ON DELETE CASCADE
)
CREATE INDEX ix_char_owner_id ON char (owner_id)

CREATE TABLE log (
	id INTEGER NOT NULL, 
	note TEXT, 
	owner_id INTEGER NOT NULL, 
	log_file BLOB, 
	char_id INTEGER, 
	start_date DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES account (id) ON DELETE CASCADE, 
	FOREIGN KEY(char_id) REFERENCES char (id) ON UPDATE CASCADE
)

CREATE INDEX ix_log_owner_id ON log (owner_id)

CREATE TABLE "match" (
	id INTEGER NOT NULL, 
	round1 BOOLEAN NOT NULL, 
	round2 BOOLEAN NOT NULL, 
	round3 BOOLEAN, 
	log_id INTEGER, 
	start_time TIME, 
	note TEXT, 
	end_time TIME, 
	PRIMARY KEY (id), 
	CHECK (round1 IN (0, 1)), 
	CHECK (round2 IN (0, 1)), 
	CHECK (round3 IN (0, 1)), 
	FOREIGN KEY(log_id) REFERENCES log (id) ON DELETE CASCADE
)
CREATE INDEX ix_match_log_id ON "match" (log_id)

CREATE TABLE match_player (
	player_id INTEGER NOT NULL, 
	match_id INTEGER NOT NULL, 
	side BOOLEAN NOT NULL, 
	PRIMARY KEY (player_id, match_id), 
	FOREIGN KEY(player_id) REFERENCES player (id) ON UPDATE CASCADE, 
	FOREIGN KEY(match_id) REFERENCES "match" (id) ON DELETE CASCADE, 
	CHECK (side IN (0, 1))
)
