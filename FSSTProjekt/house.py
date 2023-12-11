from paho.mqtt.client import Client
import time
import influxdb_client, os, time
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Q5cQfF5rXA-bfWuOz43mp96B3w2GRpv_Kdr927eEnpSavDod5Vl_9EhX8VZdX0egKJkTSzo1T6eg0osXGFffdg=="
org = "Python is Trash AG"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
query_api = write_client.query_api()

bucket = "PVInformation"




client = Client("PVPublisher")

client.connect("localhost", 1883, 60)


client.loop_start()





while True:

    query = """from(bucket: "PVInformation")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Python is Trash AG")



    time.sleep(0.5)


