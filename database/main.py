from data import data
import os
if __name__ == '__main__':
    x = data()
    x.create_tables()
    #x.generate_test_players()
    a = x.get_playerid("player1")
    b = x.insert_match(True, True, None)
    print(b)
