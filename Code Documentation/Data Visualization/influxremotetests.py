from influxdb import InfluxDBClient

json_body = [
    {
        "measurement": "cpu_load",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]

client = InfluxDBClient('192.168.0.104', 8086, 'eric', 'dragonslayer9907', 'example')

client.create_database('example')

client.write_points(json_body)

result = client.query('select value from cpu_load_short;')

print("Result: {0}".format(result))