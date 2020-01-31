#objects for log and match
import datetime

#These are not currenly used
class log():
    def __init__(self, date: datetime.datetime, matches: list):
        self.date = date
        self.matches=matches


class match():
    def __init__(self, time: datetime.datetime, matches: list):
        self.time=time
        self.matches=matches


if __name__ == "__main__":
    x= log(datetime.datetime(2000,1,10), [])


