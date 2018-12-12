from bottle import Bottle, run
from uwsgidecorators import timer
from logging import basicConfig, warning, WARNING

from .function import DiskStatus, SendMail
from mysettings import WARNING_DISK_SPACE, WARNING_INODE_SPACE
from mysettings import USERNAME_TO, USERNAME_FROM, PASSWORD, HOST_SERVER, SUBJECT
from mysettings import BASE_URL, CICLE_TIME, POINT_MOUNT

app = application = Bottle()
logger = basicConfig(filename='sensor.log', level=WARNING)


@timer(CICLE_TIME)
def send(signum):
	df = DiskStatus(POINT_MOUNT)
	free_disk = df.free_space()

	for disk_level in free_disk.values():
		# level 1 key - hostname

		for disk in disk_level.values():
			# level 2 key - mount point
			key_point = list(disk_level.keys())

			if disk['free_disk_%'] < WARNING_DISK_SPACE or \
					disk['free_inode_%'] < WARNING_INODE_SPACE:
				sendm = SendMail(USERNAME_TO, USERNAME_FROM, PASSWORD, HOST_SERVER, SUBJECT)
				sendm.send(free_disk)

				warning(
					f"Точка монтирования:  {key_point[0]} Осталось мало места на диске : {disk['free_disk_%']}%."
					f"  Свободно инодов:  {disk['free_inode_%']}% ")


@app.post(BASE_URL)
@app.route(BASE_URL, methods=['GET'])
def disk_data():
	df = DiskStatus(POINT_MOUNT)
	result = df.free_space()
	return {'disk': result}


if __name__ == '__main__':
	run(app)
