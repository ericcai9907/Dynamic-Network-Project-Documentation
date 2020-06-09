from influxdb import InfluxDBClient
import random
import uuid
import time


Host_IP = '127.0.0.1' #this is the ip address of the machine hosting database
PORT = 8086 #default port for influxdb, can be changed if necessary 
DB_Name = 'demo2' # name of used database
#measurement_name = 'm3' # name of the measurement that is being added
precision = 'ms' # time precision of the data
data_format = 'json'

client = InfluxDBClient(host=Host_IP, port=PORT)
# Host is the ip address of the machine that hosts the database
client.create_database(DB_Name)
#creates the database that will be used
def run():
	
	number_of_points = 7200 
	#10 min of data, 250000 data points will have the script running for literally days
	

	id_tags = []
	for i in range(100):
		id_tags.append(str(uuid.uuid4()))
	#creates id tags
	client_write_start_time = time.perf_counter()
	y=0
	for i in range(number_of_points):
		if y == 35:
			y=0
		else:
			y+=5

		data = [
			{
				"measurement": 'm1',
				"tags": {
				"id": random.choice(id_tags)
					},
				"fields": {
					"x": 5,
					"y": y,
				
					},
				"time": int(time.time() * 1000)
				}
			]

		client.write_points(data, database=DB_Name, time_precision=precision, protocol=data_format)
		data = [
			{
				"measurement": 'm2',
				"tags": {
				"id": random.choice(id_tags)
					},
				"fields": {
					"x": 10,
					"y": y,
				
					},
				"time": int(time.time() * 1000)
				}
			]



		client.write_points(data, database=DB_Name, time_precision=precision, protocol=data_format)
		time.sleep(.95)
	'''
	database should be the same as above, time_precision depends on the time precision you want
	this script uses the time lib and calculates time to a ms precision
	'''
	client_write_end_time = time.perf_counter()

	print("Client Library Write: {time}s".format(time=client_write_end_time - client_write_start_time))

if __name__ == '__main__':
	run()
	'''
	for i in range(100):
		run()
		time.sleep(5)
		'''