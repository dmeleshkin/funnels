import os, sys, datetime, json
from loadevents import loadEvents
from events import EventDetails, node
from common import pastMidnight
from itertools import groupby
from zipfile import ZipFile, ZIP_DEFLATED

STEPS_NUMBER = 8
SOURCE_KEY = "FROM"
SOURCE_UNKNOWN = "unknown"

events = {
	"android": [
                ("Brokerage CreateTradeOrderBuyApplicationV2 Start Click", 0),
                ("Brokerage CreateTradeOrderBuyApplicationV2 LockCheckAgreement Show", 1),
                ("Brokerage CreateTradeOrderBuyApplicationV2 LockCheckAgreement createShortApplication Click", 2),
                ("Brokerage CreateTradeOrderBuyApplicationV2 OrderParameters Show", 3),
                ("Brokerage CreateTradeOrderBuyApplicationV2 OrderParameters ValidationFail", 4),
                ("Brokerage CreateTradeOrderBuyApplicationV2 OrderParameters transfer Click", 5),
                ("Brokerage CreateTradeOrderBuyApplicationV2 Confirm Show", 6),
                ("Brokerage CreateTradeOrderBuyApplicationV2 ConfirmExitTOBuy Show", 7)
        ],
        "ios": [
                ("Brokerage CreateTradeOrderBuyApplicationV2 Start Click", 0),
                ("Brokerage createTradeOrderBuyApplicationV2 LockCheckAgreement Show", 1),
                ("Brokerage createTradeOrderBuyApplicationV2 LockCheckAgreement createShortApplication Click", 2),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters Show", 3),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters ValidationFail", 4),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters transfer Click", 5),
                ("Brokerage createTradeOrderBuyApplicationV2 confirm Show", 6),
                ("Brokerage createTradeOrderBuyApplicationV2 ConfirmExitTOBuy Show", 7)

	]
}

date = pastMidnight() - datetime.timedelta(days = 1)
if len(sys.argv) > 1:
      date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")

# Events archive
evarc = f"bonds/events{date:%Y%m%d}.zip"
# Load events
if not os.path.exists(evarc):
      loadEvents(date, events, "bonds")

# Calculate funnel

def eventsRange(platform: str, events: list, date: datetime):     
      def parseEventLine(event_line: str, event_name: str, event_step: int) -> EventDetails:
            event_parts = event_line.strip().split(',')
            params = json.loads(",".join(event_parts[2:-1]).strip('"').replace('""', '"'))

            params_from = SOURCE_UNKNOWN
            for key in params:
                  if key.upper() == SOURCE_KEY:
                        params_from = params[key]

            def getParameterValue(keys, default = ""):
                  for key in keys:
                        if key in params:
                              return params[key]
                  return default
      
            return EventDetails(
                  device = event_parts[0],
                  date = event_parts[1],
                  name = event_name,
                  step = event_step,
                  version = event_parts[-1],
                  source = params_from,
                  user = getParameterValue(["User Login ID", "USER_LOGIN_ID"]), 
                  external = getParameterValue(["External Source", "external_source"]), 
                  node = node(getParameterValue(["M_API_NODE", "mAPINode"]), getParameterValue(["M_API"])),
                  native = True,
                  )

      with ZipFile(f"bonds/events{date:%Y%m%d}.zip", "r") as z:         
            for event_name, event_step in events:
                  with z.open(f"{platform}_events/{event_name}.csv", "r") as f:
                        lines = iter(f)
                        next(lines) # Skips a first line with columns captions
                        for line in map(lambda l: l.decode("utf-8"), lines):
                              yield parseEventLine(line, event_name, event_step)

def sortedEventsRange(platform: str, events: list, date: datetime) -> EventDetails:
      device, maxStep = None, -1
      for event in sorted(eventsRange(platform, events, date), key = lambda e: f"{e.device}.{e.date}"):
            if device != event.device:
                  device, maxStep = event.device, -1
            if event.step == 0 or maxStep < event.step:
                  maxStep = event.step
                  yield event

def buildFunnel(events, date):
      device, step, source = "", -1, SOURCE_UNKNOWN
      funnel = {}
      for platform in events:
            sources, devices = {}, [0] * STEPS_NUMBER
            for el in sortedEventsRange(platform, events[platform], date):
                  if not el.source in sources:
                        sources[el.source] = {"devices": [0] * STEPS_NUMBER, "events": [0] * STEPS_NUMBER}

                  sources[el.source]["events"][el.step] += 1
                  devices[el.step] = 1
                  
                  if (device != el.device):
                        for i in range(STEPS_NUMBER):
                              sources[el.source]["devices"][i] += devices[i]
                        devices = [0] * STEPS_NUMBER
                  device, step = el.device, el.step

            funnel[platform] = sources
      return funnel

funnel = buildFunnel(events, date)
with ZipFile(f"bonds/funnel{date:%Y%m}.zip", "a", ZIP_DEFLATED) as z:
      z.writestr(f"{date:%d}", json.dumps(funnel, separators=(',', ':')))

# Build funnel report and send it
os.system(f"python3 reposell.py {date:%Y-%m-%d} >> bonds/loading.log")
# os.system(f"python3 sendmail.py {date:%Y-%m-%d} >> bonds/loading.log")

