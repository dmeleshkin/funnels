import sys, datetime, openpyxl, json, math
from common import month_name, pastMidnight, datesRange
from zipfile import ZipFile

STEPS_NUMBER = 8
STEPS = [
	"Вход в процесс",
	"Нет брокерского счета",
	"Открытие брокерского счета",
	"Параметры покупки",
	"Недостаточно средств",
	"Пополнение",
	"Подтверждение",
	"Заявление",
]


def buildExcelReport(date, funnels, sources):
	COLUMNS = ['C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH']

	COLORS = [
		{"android": ("375623", "FFFFFF"), "ios": ("372356", "FFFFFF"), "total": ("562302", "FFFFFF")},
		{"android": ("CEE4C0", "404040"), "ios": ("CEC0E4", "404040"), "total": ("E4C00E", "404040")},
		{"android": ("CEE4C0", "404040"), "ios": ("CEC0E4", "404040"), "total": ("E4C00E", "404040")},
		{"android": ("48702E", "FFFFFF"), "ios": ("482E70", "FFFFFF"), "total": ("702E04", "FFFFFF")},
		{"android": ("CEE4C0", "404040"), "ios": ("CEC0E4", "404040"), "total": ("E4C00E", "404040")},
		{"android": ("CEE4C0", "404040"), "ios": ("CEC0E4", "404040"), "total": ("E4C00E", "404040")},
		{"android": ("598B39", "FFFFFF"), "ios": ("59398B", "FFFFFF"), "total": ("8B3906", "FFFFFF")},
		{"android": ("6AA544", "FFFFFF"), "ios": ("6A44A5", "FFFFFF"), "total": ("A54408", "FFFFFF")},
		
  	{"android": ("7CB856", "FFFFFF"), "ios": ("7C56B8", "FFFFFF"), "total": ("B8560A", "FFFFFF")},
		{"android": ("90C371", "FFFFFF"), "ios": ("9071C3", "FFFFFF"), "total": ("C3710B", "FFFFFF")},
		{"android": ("A5CE8B", "000000"), "ios": ("A58BCE", "000000"), "total": ("CE8B0C", "000000")},
		{"android": ("B9D9A6", "404040"), "ios": ("B9A6D9", "404040"), "total": ("D9A60D", "404040")},
		{"android": ("CEE4C0", "404040"), "ios": ("CEC0E4", "404040"), "total": ("E4C00E", "404040")},
	]	

	weekend_font = openpyxl.styles.Font(color = "FF0000")

	wbook = openpyxl.load_workbook("funnel_template.xlsx")
	
	# Заполняет день месяца в заголовке таблицы
	def fillDayCell(sheet, column, date):
		sheet.cell(row = 2, column = 3 + i).value = date.day
		if date.weekday() > 4:
			sheet.cell(row = 2, column = 3 + i).font = weekend_font

	# Заполняет месяц и год в заголовке таблицы
	def fillMonthCell(sheet, monthes):
		for mkey in monthes:
			sheet.merge_cells(start_row=1, start_column=3 + monthes[mkey][0], end_row=1, end_column=3 + monthes[mkey][1])
			sheet.cell(row = 1, column = 3 + monthes[mkey][0], value = f"{month_name[mkey[0]]}, {mkey[1]}")

	def setCell(cell, value, fill, font):
		cell.value = value
		cell.fill = fill
		cell.font = font
	
	# Вычисляем месяцы, которые покажем в заголовках таблиц
	monthes = {}
	for i, date in enumerate(funnels):
		mkey = (date.month, date.year)
		if mkey in monthes:
			monthes[mkey][1] = i
		else:
			monthes[mkey] = [i, i]
	
  # Заполняем вкладки
	for groupby in ["events", "devices"]:
		for platform in ["android", "ios", "total"]:
			fillMonthCell(wbook[f"{platform} {groupby}"], monthes)
			for i, date in enumerate(funnels):
				fillDayCell(wbook[f"{platform} {groupby}"], i, date)
			
			# Заполняем данные по источникам
			for step in range(STEPS_NUMBER):
				step_fill = openpyxl.styles.PatternFill(fgColor = COLORS[step][platform][0], fill_type = "solid")
				step_font = openpyxl.styles.Font(color = COLORS[step][platform][1])

				# Вычисляет номер строки для текущего шага и заданного номера источника
				def getrow(source_n = len(sources)):
					return 3 + source_n + step * (1 + len(sources))

				# Заполняем названия шагов и источников
				wbook[f"{platform} {groupby}"].merge_cells(start_row = getrow(0), start_column = 1, end_row = getrow(len(sources)), end_column = 1)
				setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(0), column = 1), STEPS[step], step_fill, step_font)
				for num, source in enumerate(sources):
					setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(num), column = 2), source, step_fill, step_font)
				setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(), column = 2), "по всем источникам", step_fill, step_font)

				# Заполняем значения 
				if platform == "total":
					for day, date in enumerate(funnels):
						for num, source in enumerate(sources):
							def getFormula(n = len(sources)):							
								cell = f'{COLUMNS[day]}{getrow(n)}'
								# return f'=IF(android!{cell} + ios!{cell} > 0, android!{cell} + ios!{cell}, "")'
								return f"='android {groupby}'!{cell} + 'ios {groupby}'!{cell}"
							setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(num), column = 3 + day), getFormula(num), step_fill, step_font)
						setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(), column = 3 + day), getFormula(), step_fill, step_font)
				else:
					for day, date in enumerate(funnels):
						funnel, source_total = funnels[date][platform], 0
						for num, source in enumerate(sources):
							source_value = funnel[source][groupby][step] if source in funnel else 0
							source_total += source_value
							setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(num), column = 3 + day), source_value, step_fill, step_font)
						setCell(wbook[f"{platform} {groupby}"].cell(row = getrow(len(sources)), column = 3 + day), source_total, step_fill, step_font)
			
			# Добавляем фильтр по источникам
			wbook[f"{platform} {groupby}"].auto_filter.ref = f"B2:B{STEPS_NUMBER * (1 + len(sources)) + 2}"		
	wbook.save(f'bonds/reports/funnel{date:%Y%m%d}.xlsx')

def funnelDatesRange(finish: datetime):
	if finish.day > 28:
		return datesRange(datetime.datetime(finish.year, finish.month, 1), finish)
	
	if finish.month == 1:
		return datesRange(datetime.datetime(finish.year - 1, 12, finish.day), finish)

	return datesRange(datetime.datetime(finish.year, finish.month - 1, finish.day), finish)

def enumerateSources(funnels):
	for dayFunnel in funnels.values():
		for platformFunnel in dayFunnel.values():
			for source in platformFunnel.keys():
				yield source

def getFunnel(date: datetime):
	with ZipFile(f"bonds/funnel{date:%Y%m}.zip", "r") as z:
		return json.loads(z.read(f"{date:%d}"))

date = pastMidnight() - datetime.timedelta(days = 1)
funnels = dict([(d, getFunnel(d)) for d in funnelDatesRange(date)])
sources = set(enumerateSources(funnels))
buildExcelReport(date, funnels, sources)

