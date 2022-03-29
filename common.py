import datetime

month_name = ["", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
month_name2 = ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
weekdays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"] 

def pastMidnight() -> datetime:
	now = datetime.datetime.now()
	return datetime.datetime(now.year, now.month, now.day)

def datesRange(start: datetime, finish: datetime, delta = datetime.timedelta(days = 1)):
      if start >= finish:
            while start >= finish:
                  yield start
                  start -= delta
      else:
            while start <= finish:
                  yield start
                  start += delta
