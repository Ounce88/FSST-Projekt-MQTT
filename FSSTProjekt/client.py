from paho.mqtt.client import Client
import time

from influxdb import InfluxDBClient
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "L1XwTzFrMM-v3LiWuCMknySKtoJPH_ay_OBfQ8isTl6Q7lUDJ81SxTBh6iFQJPYuiwDqj3LNtXtYBzteSVj1qg=="
org = "Lindinger"
url = "http://localhost:8086"

broker = "localhost"  # Oder die IP-Adresse deines Brokers, falls er nicht lokal läuft
port = 1883
topic = "sinus/topic"

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
    write_api.write(bucket=bucket, org="Lindinger", record=point)


client = Client("SinusSubscriber")

client.connect(broker, port)


client.subscribe(topic)
client.on_message = ReceiveSinus

client.loop_start()


while True:


    query = """from(bucket: "Sinus")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Lindinger")



    time.sleep(0.5)
