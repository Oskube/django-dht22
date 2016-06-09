import serial

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from dht22.models import Sensordata

class Command(BaseCommand):
	help = 'Reads DHT22 readings from specified port'

	def add_arguments(self, parser):
		parser.add_argument('port', type=str)
	def handle(self, *args, **kwargs):
		port = kwargs['port']
		self.stdout.write("Trying to open and read port: %s" % port);
		
		ser = serial.Serial(port, 9600, timeout=60)
		if ser.is_open:
			data = ser.readline().decode().strip('\n\r').split(';')
			print("HUM: {0}\tTemp:{1}".format(data[0], data[1]))
			ser.close()
			db = Sensordata(humidity=data[0], temperature=data[1], time=timezone.now())
			db.save()
		else:
			self.stdout.write("Failed to open port");
