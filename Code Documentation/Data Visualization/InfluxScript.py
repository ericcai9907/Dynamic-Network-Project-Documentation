from influxdb import InfluxDBClient
import random
import uuid
import time
import datetime

client = InfluxDBClient(host='127.0.0.1', port=8086)
# Host is the ip address of the machine that hosts the database
client.create_database('script_tests2')
#creates the database that will be used
def run():
	measurement_name = 'm1'
	#name of the measurement 
	number_of_points = 250000
	#data_end_time = int(time.time() * 1000) #milliseconds

	id_tags = []
	for i in range(100):
	    id_tags.append(str(uuid.uuid4()))
	#creates id tags

	data = []
	data.append(
	        {
	                "measurement": measurement_name,
	                "tags": {
	                        "id": random.choice(id_tags)
	                },
	                "fields": {
	                        "x": round(random.random(),4),
	                        "y": round(random.random(),4),
	                        "z": random.randint(0,50)
	                },
	                "time": int(time.time()*1000)
	        }
	)
	current_point_time = data_end_time

	for i in range(number_of_points-1):
	        current_point_time = current_point_time - random.randint(1,100)
	        data.append(
	                {
	                        "measurement": measurement_name,
	                        "tags": {
	                                "id": random.choice(id_tags)
	                        },
	                        "fields": {
	                                "x": round(random.random(),4),
	                                "y": round(random.random(),4),
	                                "z": random.randint(0,50)
	                        },
	                        "time": int(time.time() * 1000)
	                }
	        )


	client_write_start_time = time.perf_counter()

	client.write_points(data, database='script_tests2', time_precision='ms', batch_size=10000, protocol='json')
	'''
	database should be the same as above, time_precision depends on the time precision you want
	this script uses the time lib and calculates time to a ms precision
	'''
	client_write_end_time = time.perf_counter()

	print("Client Library Write: {time}s".format(time=client_write_end_time - client_write_start_time))

if '__name__' == '__main__':
	run()
	'''
	for i in range(100):
		run()
		time.sleep(5)
		'''