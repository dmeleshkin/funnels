import datetime

def pastMidnight() -> datetime:
	now = datetime.datetime.now()
	return datetime.datetime(now.year, now.month, now.day)
