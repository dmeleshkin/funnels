import sys, datetime
from loadevents import loadEvents
from common import pastMidnight

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

date = pastMidnight() - datetime.timedelta(days = 1)
if len(sys.argv) > 1:
      date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")

loadEvents(date, events, "bonds")

