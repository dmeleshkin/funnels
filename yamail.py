import smtplib, re, base64
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.header import Header
from email.utils import formataddr

class yamail(object):
	def __init__(self, user, token, host="smtp.yandex.com", port=465, debug=False):
		auth = u'user={0}\@yandex.ru\001auth=Bearer {1}\001\001'.format(user, token)
		# auth = f"user={user}\@yandex.ru\001auth=Bearer {token}\001\001"
		self._auth = "AUTH XOAUTH2 " + base64.b64encode(auth.encode('utf8')).decode('utf-8')
		self._host = host
		self._port = port
		self._debug = debug		
		self._attachments = []
		self._recipients = []

	def _addr(self, address, alias=None):
		assert re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", address)
		return formataddr((str(Header(alias, 'utf-8')), address)) if alias else address

	def sender(self, address, alias=None):
		self._sender = self._addr(address, alias)

	
	def recipient(self, address, alias=None):
		self._recipients.append(self._addr(address, alias))

	def attach(self, filepath):
		self._attachments.append(filepath)

	def send(self, subject, body):
		msg = MIMEMultipart()
		msg['From'] = self._sender
		msg['To'] = COMMASPACE.join(self._recipients)
		msg['Date'] = formatdate(localtime=True)
		if subject:
			msg['Subject'] = str(Header(subject, 'utf-8'))
		if body:
			msg.attach(MIMEText(body, _charset="UTF-8"))

		for a in self._attachments:
			with open(a, "rb") as f:
				part = MIMEApplication(f.read(), Name=basename(a))
			# After the file is closed
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(a)
			msg.attach(part)	
	
		smtp = smtplib.SMTP_SSL(self._host, self._port)
		if self._debug:
			smtp.set_debuglevel(1)
		smtp.ehlo()
		if self._auth:
			smtp.docmd(self._auth)
		smtp.sendmail(self._sender, self._recipients, msg.as_string())
		smtp.close()
