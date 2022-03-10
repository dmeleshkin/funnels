import sys, os, requests, datetime, time, shutil
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	
def loadEvents(date, events, workingdir):
	def getToken() -> str:
		with open("settings/.token") as f:
			return f.read().strip()
	
	def buildPath(path: str) -> str:
		if not os.path.exists(path):
			os.makedirs(path)
		return path

	def loadEvent(token, platform, date_since, date_until, event_name, fout, silent = False):
		appId = {"android": "187690", "ios": "187675"}[platform]
		dateformat = "%Y-%m-%d%%20%H%%3A%M%%3A%S"
		d1, d2 = date_since.strftime(dateformat), date_until.strftime(dateformat)
		url = f"https://api.appmetrica.yandex.ru/logs/v1/export/events.csv?application_id={appId}&date_since={d1}&date_until={d2}&date_dimension=default&use_utf8_bom=true&fields=appmetrica_device_id%2Cevent_datetime%2Cevent_json%2Capp_version_name&event_name={event_name}"

		megabyteSize=1048576
		bytesCount = 0
		megabytesCount = 0
		while True:
			with requests.get(url, headers={"Authorization": "OAuth " + token}, stream=True, verify=False) as r:
				if r.status_code == 200:
					r.raise_for_status()
					with open(fout, 'wb') as f:
						for chunk in r.iter_content(chunk_size=megabyteSize):
							if chunk:
								f.write(chunk)
								if not silent:
									bytesCount += len(chunk)		                
									if megabytesCount != bytesCount // megabyteSize:
										megabytesCount = bytesCount // megabyteSize
										print("{}Mb load".format(megabytesCount))
					if not silent:
						print('file has been dowload')
					return r.status_code
				elif r.status_code == 202:
					if not silent:
						print(datetime.datetime.now().strftime("%H:%M"), "-", r.status_code, "-", r.text)
					time.sleep(100)
				else:
					if not silent:
						print(r.status_code, ": ", r.text)
					return r.status_code

	token = getToken()
	total, success, fails = 0, 0, 0
	for tries in range(3):
		total, success, fails = 0, 0, 0
		print(f"\n\n{date} start loading... {tries} try...\n\n")

		for platform in events:
			path = buildPath(f"{workingdir}/{date:%Y%m%d}/{platform}_events")
			for event_name, _ in events[platform]:
				event_file = f"{path}/{event_name}.csv"
				if not os.path.exists(event_file):
					print(f"{platform}, {event_name}:")
					total += 1
					try:
						if 200 == loadEvent(token, platform, date, date + datetime.timedelta(hours = 26), event_name, event_file):
							success += 1
						else:
							fails += 1
					except: # TimeoutError most often
						print("Loading failed with exception")
						fails += 1

		print(f"\n\n {date} load successfully\n\n{success} files form {total} load successfully, fails {fails}")
		
		if fails == 0:
			break
		time.sleep(2000)

	if fails == 0:
		# Comress data and remove sources
		datapath = f"{workingdir}/{date:%Y%m%d}"
		shutil.make_archive(f"{workingdir}/events{date:%Y%m%d}", 'zip', datapath)
		shutil.rmtree(datapath)

