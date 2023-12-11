from paho.mqtt.client import Client
import time

from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Q5cQfF5rXA-bfWuOz43mp96B3w2GRpv_Kdr927eEnpSavDod5Vl_9EhX8VZdX0egKJkTSzo1T6eg0osXGFffdg=="
org = "Python is Trash AG"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
query_api = write_client.query_api()

bucket = "Sinus"

def ReceiveSinus(client, userdata, message):
    value = float(message.payload.decode())
    print("Received Sinus, Value:", value)
    point = (
        Point("Received")
        .tag("Sin_Val", "Value")
        .field("MeasurementPoint", value)
    )
    write_api.write(bucket=bucket, org="Python is Trash AG", record=point)


client = Client("SinusSubscriber")

client.connect("localhost", 1883, 60)


client.subscribe("sinus/topic")
client.on_message = ReceiveSinus

client.loop_start()


while True:


    query = """from(bucket: "Sinus")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Python is Trash AG")



    time.sleep(0.5)