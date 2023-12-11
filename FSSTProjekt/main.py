import math
import time
import paho.mqtt.client as mqtt


broker = "localhost"  # Oder die IP-Adresse deines Brokers, falls er nicht lokal läuft
port = 1883
topic = "sinus/topic"


def calculate_sin_value(phase, amplitude=1):
    return amplitude * math.sin(phase)

client = mqtt.Client("SinusPublisher")
client.connect(broker, port)


phase = 0
while True:
    sin_value = calculate_sin_value(phase)
    client.publish(topic, payload=sin_value)
    phase += 0.1  # Erhöht die Phase für den nächsten Wert
    time.sleep(0.5)  # Warte 0,5 Sekunden bis zum nächsten Wert