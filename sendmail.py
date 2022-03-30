import sys, os, json
import yamail
from common import pastMidnight

mailSettings = ""
attachment = False
bodyParams = []

for arg in sys.argv[1:]:
	if arg.startswith(f"-mail:"):
		mailSettings = arg[6:]
	elif arg.startswith(f"-attachment:"):
		attachment = arg[12:]
	else:
		bodyParams.append(arg)


def getToken() -> str:
	with open("settings/.token") as f:
		return f.read().strip()

if os.path.exists(mailSettings):
	with open(mailSettings, "r") as f:
		mailParams = json.load(f)

		mail = yamail.yamail(mailParams["user"], getToken())
		mail.sender(mailParams["sender"], mailParams["alias"])
		for recipient in mailParams["to"]:
			mail.recipient(recipient[0], recipient[1])

		if attachment and os.path.exists(attachment):
			mail.attach(attachment)

		body = mailParams["body"]
		if len(bodyParams) > 0:
			body = body.format(*tuple(bodyParams))
		mail.send(mailParams["subject"], body)

