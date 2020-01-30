
def win_pre(matches :list):
    wins = 0
    loss = 0

    for match in matches:
        if(match == None):
            continue
        if(match == 1):
            wins+=1
        if(match == 0):
            loss+=1
    
    return wins/(wins+loss)