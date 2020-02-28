from .event import Event

class Ranked_wz(Event):
    def __init__(self, start, end, location, rows, team: list, opponent: list, number=0):
        super(Ranked_wz, self).__init__(start, end, location, rows)
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3
        self.team = team
        self.opponent = opponent
        self.number = number

    def find_team_opponent(row_object: Row, team: list, opponents: list, owner):
        if row_object.target == row_object.source:  # saves time
            return

            # Starter buffs hunters, mark, Coordination and might are the diffrent types of buffs players can apply to their team mates (and only their team mates)"
        if "Hunter's Boon" in row_object.ability_name or "Mark of Power" in row_object.ability_name or "Coordination" in row_object.ability_name or "Unnatural Might" in row_object.ability_name:

            # appending to team the target or source that is not owner (and not already in the list)
            if row_object.target != owner and row_object.target not in team and row_object.target:
                team.append(row_object.target)
            elif row_object.source not in team and row_object.source != owner and row_object.source:
                team.append(row_object.source)
            return

            # appending to enemies the target or source that is not owner (and not already in the list)
        if "Damage" in row_object.details:
            if row_object.target != owner and row_object.target not in opponents and row_object.target:
                opponents.append(row_object.target)
            elif row_object.source not in opponents and row_object.source != owner and row_object.source:
                opponents.append(row_object.source)
            return

            # appending to team list, the row target or souce, depending on which is not owner (and not already in the list)
        if "Heal" in row_object.details:
            if row_object.target != owner and row_object.target not in team and row_object.target:
                team.append(row_object.target)
            elif row_object.source not in team and row_object.source != owner and row_object.source:
                team.append(row_object.source)
            return
      