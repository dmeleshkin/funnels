import os, datetime
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

# def isFileInList(fname, flist):
#       for f, _ in flist:
#             if fname.startswith(f):
#                   return True
#       return False

for date in datesRange(datetime.datetime(2022, 3, 23), datetime.datetime(2022, 2, 1)):
      # print(f"mv events{date:%Y%m%d} {date:%Y%m%d}")
      os.system(f"python3 bonds.py {date:%Y-%m-%d} >> bonds/loading.log")

      # zippath = f"../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}.zip"
      # if os.path.exists(zippath):
      #       os.system(f"unzip {zippath} -d ../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}/")

      # for platform in events:
      #       pfolder = f"../yambroFunnelOpenDaily/data/bonds/events{date:%Y%m%d}/{platform}_events"
      #       if os.path.exists(pfolder):
      #             for fname in os.listdir(pfolder):
      #                   if not isFileInList(fname, events[platform]):
      #                         os.remove(f"{pfolder}/{fname}")
      #                         print(f"Removed file: {pfolder}/{fname}")

      # loadEvents(date, events, "../yambroFunnelOpenDaily/data/bonds")

