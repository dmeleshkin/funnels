import sys, datetime
from loadevents import loadEvents
from common import datesRange

events = {
	"android": [
                ("Brokerage CreateTradeOrderBuyApplicationV2 Start Click", 0),
                ("Brokerage CreateTradeOrderBuyApplicationV2 LockCheckAgreement Show", 1),
                ("Brokerage CreateTradeOrderBuyApplicationV2 LockCheckAgreement createShortApplication Click", 2),
                ("Brokerage CreateTradeOrderBuyApplicationV2 OrderParameters Show", 3),
                ("Brokerage СreateTradeOrderBuyApplicationV2 OrderParameters ValidationFail", 4),
                ("Brokerage CreateTradeOrderBuyApplicationV2 OrderParameters transfer Click", 5),
                ("Brokerage CreateTradeOrderBuyApplicationV2 Confirm Show", 6),
                ("Brokerage CreateTradeOrderBuyApplicationV2 ConfirmExitTOBuy Show", 7)
        ],
        "ios": [
                ("Brokerage CreateTradeOrderBuyApplicationV2 Start Click", 0),
                ("Brokerage createTradeOrderBuyApplicationV2 LockCheckAgreement Show", 1),
                ("Brokerage createTradeOrderBuyApplicationV2 LockCheckAgreement createShortApplication Click", 2),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters Show", 3),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters ValidationFail", 3),
                ("Brokerage createTradeOrderBuyApplicationV2 OrderParameters transfer Click", 4),
                ("Brokerage createTradeOrderBuyApplicationV2 confirm Show", 5),
                ("Brokerage createTradeOrderBuyApplicationV2 ConfirmExitTOBuy Show", 6)

	]
}


for date in datesRange(datetime.datetime(2022, 3, 6), datetime.datetime(2022, 1, 20)):
      zippath = f"../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}.zip"
      if os.path.exists(zippath):
            os.system(f"unzip {zippath} -d ../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}/")

      for platform in events:
            pfolder = f"../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}/{platform}_events"
            if os.path.exists(pfolder):
                  for f in os.listdir(pfolder):
                        fname = f.split("/")[-1]
                        print(f"{f}\t\t{fname}")

      # loadEvents(date, events, "../yambroFunnelOpenDaily/data/bonds")

