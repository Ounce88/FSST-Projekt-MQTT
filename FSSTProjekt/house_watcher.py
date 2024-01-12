import json

from influxdb_client import Point
from paho.mqtt.client import Client
import time
import influxdb_client, os, time
from influxdb_client.client.write_api import SYNCHRONOUS

token = "4yUnNQCoPi_cs_QpCNQa-Xq_MeYY8mzb6AnJDUjqR5KBe_oJKrIrOHJCqebYf87Z8MAXPMHRATRdtQZ8kywP2g=="
org = "Lindinger"
url = "http://localhost:8086"

broker = "localhost"  # Oder die IP-Adresse deines Brokers, falls er nicht lokal läuft
port = 1883
topic = "house/pv"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
query_api = write_client.query_api()

bucket = "PVInformation"
client = Client("PVReceiver")
client.connect(broker, port)
client.subscribe(topic)
pvProduction = 0.0
verbrauch = 0.0
AutarkikPercentage = 0.0

count = 0
AutarkikCount = 0

def ReceiveHouseValues(client, userdata, message):
    global count
    global AutarkikCount

    data = json.loads(message.payload.decode())

    point = Point("pv")
    for key, value in data.items():
        if key != 'time':
            point.field(key, float(value))
            if key == "PV Produktion":
                pvProduction = float(value)
                count = count+0.5
            elif key == "Verbrauch":
                verbrauch = float(value)
                count = count + 0.5

    print("Received House, Value:", value)

    point.field("ProductionMinusUsage", float(verbrauch - pvProduction))
    print("ProductionMinusUsage", float(verbrauch - pvProduction))
    if pvProduction >= verbrauch:
        AutarkikCount += 1

    if count > 0:
        AutarkikPercentage = (AutarkikCount / count) * 100
        point.field("AutarkikPercentage", AutarkikPercentage)
        print("AutarkikPercentage", float(AutarkikPercentage))
    write_api.write(bucket=bucket, org="Lindinger", record=point)




client.on_message = ReceiveHouseValues
client.loop_start()

while True:

    query = """from(bucket: "PVInformation")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Lindinger")
    time.sleep(1)



