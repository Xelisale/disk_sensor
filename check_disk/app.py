from bottle import Bottle, run
from uwsgidecorators import timer
from logging import basicConfig, warning,  WARNING

from .function import DiskStatus, SendMail
from settings import WARNING_DISK_SPACE, WARNING_INODE_SPACE
from settings import USERNAME_TO, USERNAME_FROM, PASSWORD, HOST_SERVER, SUBJECT
from settings import BASE_URL


app = application = Bottle()
logger = basicConfig(filename='sensor.log', level=WARNING)


@timer(100)
def send(signum):
	df = DiskStatus()
	free_disk = df.free_space()
	print(free_disk)

	if free_disk['free_disk_percent'] < WARNING_DISK_SPACE or \
		free_disk['free_inode_percent'] < WARNING_INODE_SPACE:

		sendm = SendMail(USERNAME_TO, USERNAME_FROM, PASSWORD, HOST_SERVER, SUBJECT)
		sendm.send(free_disk)

		warning(
			"Осталось мало места на диске : {0} %.  Свободно инодов:  {1}% ".format(free_disk['free_disk_percent'],
																				free_disk['free_inode_percent']))


@app.post(BASE_URL)
@app.route(BASE_URL, methods=['GET'])
def disk_data():
	df = DiskStatus()
	result = df.free_space()
	return {'disk': result}


if __name__ == '__main__':
	run(app)
