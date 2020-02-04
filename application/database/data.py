from application import db


class Account(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(144), nullable=False)
     password = db.Column(db.String(144), nullable=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    log = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime)

class Match_Player(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), primary_key=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round1 =db.Column(db.Boolean, nullable=False)
    round2 =db.Column(db.Boolean, nullable=False)
    round3 =db.Column(db.Boolean, default= None)
    log_id = db.Column(db.Integer, db.ForeignKey("log.id"))
    timestamp = db.Column(db.DateTime)
    
    players = db.relationship('Player', secondary = 'match_player')

class Player(db.Model):
    name = db.Column(db.String(30), nullable = False)
    id = db.Column(db.Integer, primary_key=True)
    matches = db.relationship('Match', secondary = 'match_player.__table__')




# CREATE TABLE IF NOT EXISTS User (
#        username varchar(20) NOT NULL,
#        password varchar(30) NOT NULL,
#        id INTEGER PRIMARY KEY NOT NULL
       
# );
# CREATE TABLE IF NOT EXISTS Log (
#        id INTEGER PRIMARY KEY NOT NULL,
#        ownerID int NOT NULL,
#        log BLOB,
#        date DATE,       
#        FOREIGN KEY(ownerID) REFERENCES User(id)
# );

# CREATE TABLE IF NOT EXISTS Player (
#        name varchar(20) NOT NULL,
#        id INTEGER PRIMARY KEY NOT NULL
       
# );

# CREATE TABLE IF NOT EXISTS Match (
#        id INTEGER PRIMARY KEY NOT NULL,
#        round1 boolean NOT NULL,
#        round2 boolean NOT NULL,
#        round3 boolean,
#        logID int,
#        timestamp DATETIME, 
#        FOREIGN KEY(logID) REFERENCES log(id)
            
# );


# CREATE TABLE IF NOT EXISTS match_player (
#        matchID int,
#        playerID int,
#        side boolean NOT NULL,
#        FOREIGN KEY(matchID) REFERENCES match(id),
#        FOREIGN KEY(playerID) REFERENCES player(id)
# );
