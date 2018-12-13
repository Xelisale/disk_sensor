from os import statvfs
from platform import uname
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPAuthenticationError


class DiskStatus:
	def __init__(self, point_mount):
		self.hostname = uname().node
		self.free_disk = {self.hostname: {}}
		self.point_mount = point_mount

	def free_space(self):
		for point in self.point_mount:

			stat = statvfs(point)
			free = round(stat.f_bavail * stat.f_bsize / 1024 / 1024)
			total_space = round(stat.f_blocks * stat.f_bsize / 1024 / 1024)
			free_percent = round((free / total_space) * 100)
			free_inode_percent = round(100 - (float(stat.f_files - stat.f_ffree) / stat.f_files) * 100)

			self.free_disk[self.hostname][point] = {
					'free_disk_mb': free,
					'free_disk_%': free_percent,
					'free_inode': stat.f_ffree,
					'free_inode_%': free_inode_percent,
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
		for disk_level in free.values():
			# level 1 key - hostname
			key_host = list(free.keys())

			for disk in disk_level.values():
				# level 2 key - mount point
				key_point = list(disk_level.keys())

				msg = "Hostname: {0}. Остаток места на диске : {1}%"
				f" Точка монтирования \'{2}\'. Свободно инодов: {3}%".format(key_host[0],
																			disk['free_disk_%'],
																			key_point[0],
																			disk['free_inode_%'])
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
