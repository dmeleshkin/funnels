import datetime

def pastMidnight() -> datetime:
	now = datetime.datetime.now()
	return datetime.datetime(now.year, now.month, now.day)

def datesRange(start: datetime, finish: datetime, delta = datetime.timedelta(days = 1)):
      while start >= finish:
            yield start
            start -= delta
