from os import statvfs
from platform import uname
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPAuthenticationError


class DiskStatus:
	def __init__(self):
		self.free_disk = []
		self.where_space = '/'

	def free_space(self):
		stat = statvfs(self.where_space)
		free = round(stat.f_bavail * stat.f_bsize / 1024 / 1024)
		total_space = round(stat.f_blocks * stat.f_bsize / 1024 / 1024)
		free_percent = round((free / total_space) * 100)
		free_inode_percent = round(100 - (float(stat.f_files - stat.f_ffree) / stat.f_files) * 100)

		self.free_disk = {
			'node': uname().node,
			'free_disk': free,
			'free_disk_percent': free_percent,
			'free_inode': stat.f_ffree,
			'free_inode_percent': free_inode_percent,
		}
		return self.free_disk


class SendMail:
	def __init__(self, username_to, username_from, password, host_server, subject):
		"""
		:param username_from - login in email
		:param username_to - email address to send
		:param password - password mail account
		:param host_server - smtp server
		:param subject - title mail
		"""
		self.username_to = username_to
		self.username_from = username_from
		self.password = password
		self.host_server = host_server
		self.subject = subject

	def send(self, free):
		msg = "{2} : Осталось мало места на диске : {0} %. Свободно инодов:  {1}% " \
			.format(free['free_disk_percent'], free['free_inode_percent'], free['node'])

		text = MIMEText(msg, "", _charset="utf-8")
		text["SUBJECT"] = self.subject
		text["FROM"] = self.username_from
		text["TO"] = self.username_to
		server = SMTP_SSL(self.host_server, 465)

		try:
			server.login(self.username_to, self.password)

		except SMTPAuthenticationError:
			print('Неверный логин или пароль')
			exit()

		server.sendmail(self.username_from, self.username_to, text.as_string())
		server.quit()
