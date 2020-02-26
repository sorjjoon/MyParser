from sqlalchemy.types import Time


class match():
    def __init__(self, start: Time, end: Time, round1, round2, round3, team: list, opponent: list, number=0, error=None, note=None, id=None, team_string=None, opponent_string=None):

        self.start = start
        self.end = end
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3
        self.team = team
        self.opponent = opponent
        self.note = note
        self.id = id
        # used by jinja templates
        self.error = error
        self.start_string = str(start)[:-10]  # removing ms from time string
        self.end_string = str(end)[:-10]
        self.number = number
        if not team_string and not opponent_string:
            self.team_string, self.opponent_string = create_list_strings(
                team, opponent)
        else:
            self.team_string = team_string
            self.opponent_string = opponent_string

    def validate(self):  # validate that this match has valid round 1, 2 and 3 values, if not, add an error string to this object
        if self.round3 is None:
            if self.round2 == self.round1:
                return True
            else:
                self.error = "Round 3 wasn't played, rounds 1 and 2 must be the same"
                return False
        else:
            if self.round1 != self.round2:
                return True
            else:
                self.error = "Round 3 was played, rounds 1 and 2 can't be the same"
                return False

    def set_rounds(self, round1, round2, round3=None):
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3


def create_list_strings(team, opponent):
    from application import db  # importing here to avoid circular

    players = db.get_char_class_by_name(team+opponent)
    team_string = []
    opponent_string = []
    # TODO make concatenate more effective
    for player_tuple in players:
        if player_tuple[0] in team:
            team_string.append(player_tuple[0] + " ("+player_tuple[1]+")")
        else:
            opponent_string.append(player_tuple[0] + " ("+player_tuple[1]+")")

    # adding ? to the list to indicate lack of players ( couldn't determine automatically)
    while len(team_string) < 3:
        team_string.append("?")

    while len(opponent_string) < 4:
        opponent_string.append("?")
    return str(team_string)[:-1][1:].replace("'", "").replace('"', ""), str(opponent_string)[:-1][1:].replace("'", "").replace('"', "")
