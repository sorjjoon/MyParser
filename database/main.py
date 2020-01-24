from data import data
import os
#main for testing the db
if __name__ == '__main__':
    x = data()
    x.create_tables()
   # x.generate_test_data()
    a = x.get_playerid("player1")
    x.insert_log(1, [(False, True, None)])
    print(a)
    x.delete_log(1)
    for x in x.get_matches([1]):
        print(x)
        
